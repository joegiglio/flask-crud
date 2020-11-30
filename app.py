# Flask-Mail reference: https://www.youtube.com/watch?v=vF9n248M1yk

from flask import Flask, render_template, redirect, url_for, request, flash, session, render_template_string
from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField, PasswordField, BooleanField, TextAreaField, SelectField, HiddenField, IntegerField
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms.validators import InputRequired, Email, Length, NumberRange, EqualTo, Regexp, DataRequired
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import exc, func, MetaData
from utils import session_dump, send_verification_email
from flask_migrate import Migrate
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import URLSafeTimedSerializer, SignatureExpired, BadTimeSignature, BadSignature
# from flask_mail import Mail, Message
from strings import greeting
import config


# Unused but may need them later!

#from decorators import session_required, admin_required, session_required_obj, session_required_review


app = Flask(__name__)
app.config.from_pyfile("config.py")
#mail = Mail(app)

s = URLSafeTimedSerializer(app.config['SECRET_KEY'])
db = SQLAlchemy(app)
migrate = Migrate(app, db)

#   TODO: Move models to separate file.  I was having inheritance issues with db.create_all.  Need to revisit.

#Form Models


class SampleForm(FlaskForm):
    username = StringField('Username',
                           validators=[
                               InputRequired(),
                               Length(message="Username must be between 4 and 20 characters",
                                      min=4, max=20)
                           ])


class LoginForm(FlaskForm):
    username = StringField('Username',
                           validators=[
                               InputRequired()
                           ])
    password = PasswordField('Password', validators=[
                                InputRequired()
                            ])
    remember = BooleanField('Remember Me for 30 days')


class CreateUserForm(FlaskForm):
    email = StringField('Email Address', validators=[
        InputRequired(),
        Email(message="Invalid email address."),
        Length(message="Email address must be between 5 and 50 characters",
               min=5, max=50)
    ])

    username = StringField('Username', validators=[
        InputRequired(),
        Length(message="Username must be between 4 and 20 characters",
               min=4, max=20)
    ])

    level = SelectField('User Level', choices=[
        ("100", "Regular User"),
        ("200", "Admin"),
        ("300", "Super Admin")
    ])


class EditUserForm(CreateUserForm):
    pass


class RegisterUserForm(FlaskForm):
    email = StringField('Email Address', validators=[
        InputRequired(),
        Email(message="Invalid email address."),
        Length(message="Email address must be between 5 and 50 characters",
               min=5, max=50)
    ])

    username = StringField('Username', validators=[
        InputRequired(),
        Length(message="Username must be between 4 and 20 characters",
               min=4, max=20)
    ])

    password = PasswordField('Password', validators=[
        InputRequired(),
        Length(message="Password must be between 5 and 50 characters",
               min=5, max=50)
    ])

    verify_password = PasswordField('Verify Password', validators=[
        InputRequired(),
        EqualTo('password', message="Passwords must match."),
        Length(message="Password must be between 5 and 50 characters",
               min=5, max=50)
    ])


class ValidateEmailForm(FlaskForm):
    email = StringField('Email Address', validators=[
        InputRequired(),
        Email(message="Invalid email address."),
        Length(message="Email address must be between 5 and 50 characters",
               min=5, max=50)
    ])


class UserSortForm(FlaskForm):
    sort_by = SelectField('Sort By', choices=[
        ("id_d", "Newest"),
        ("id", "Oldest"),
        ("username", "Username"),
        ("username_d", "Username Descending"),
        ("level", "Level"),
        ("level_d", "Level Descending"),
    ])


class CreateDogForm(FlaskForm):
    name = StringField('Name', validators=[
        InputRequired(),
        Length(message="Name must be between 1 and 20 characters",
               min=1, max=20)
    ])

    age = IntegerField('Age', validators=[
        InputRequired(),
        NumberRange(message="Age must be between 1 and 30",
                    min=1, max=30)
    ])

    breed = StringField('Breed', validators=[
        InputRequired(),
        Length(message="Breed must be between 1 and 20 characters",
               min=1, max=20)
    ])


class EditDogForm(CreateDogForm):
    pass


class DogSortForm(FlaskForm):
    sort_by = SelectField('Sort By', choices=[
        ("id_d", "Newest"),
        ("id", "Oldest"),
        ("name", "Name"),
        ("name_d", "Name Descending"),
        ("age", "Lowest Age"),
        ("age_d", "Highest Age"),
        ("breed", "Breed"),
        ("breed_d", "Breed Descending"),
    ])


#DB Models


class User(db.Model):
    # __table_args__ = {'sqlite_autoincrement': True}
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime())
    username = db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False, server_default='')
    email = db.Column(db.String(255), nullable=False, unique=True)
    verification_token = db.Column(db.String(100), nullable=False)
    confirmed_at = db.Column(db.DateTime())
    login_count = db.Column(db.Integer, server_default='0')
    last_active = db.Column(db.DateTime())
    level = db.Column(db.Integer)
    active = db.Column(db.Boolean(), nullable=False, server_default='0')
    # notification_optin = db.Column(db.Boolean, server_default='1', default=True)
    # pw_reset_token = db.Column(db.String(50))


class Dog(db.Model):
    # __table_args__ = {'sqlite_autoincrement': True}
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime())
    name = db.Column(db.String(20), nullable=False, unique=True)
    age = db.Column(db.Integer)
    breed = db.Column(db.String(20), nullable=False)


@app.route('/', methods=['GET', 'POST'])
def index():

    # The 'greeting' string comes from one of the imports.

    return render_template('index.html', title="Homepage", greeting=greeting)


@app.route('/login/', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    #request.method == 'POST':

    if form.validate_on_submit():
        username = form.username.data.strip()
        password = form.password.data.strip()

        #  Check for existence of matching username and password.
        #  Commented so we can use hashed passwords.
        #user = User.query.filter(User.username == username, User.password == password).first()

        user = User.query.filter(User.username == username).first()

        if user and check_password_hash(user.password, password):
            if user.active:
                try:
                    user.login_count = user.login_count + 1
                    user.last_active = datetime.utcnow()
                    db.session.commit()

                    session["user_id"] = user.id
                    session["user_level"] = user.level

                except exc.IntegrityError:
                    flash(u'DB Integrity error.', 'alert-danger')  # Should never occur since we already check for dupes.
                    return render_template('login.html', form=form, title="Login")
                except exc.OperationalError:
                    flash(u'DB failure.', 'alert-danger')  # Is DB down?  Does table exist?
                    return render_template('login.html', form=form, title="Login")
                except Exception as e:
                    print(e)
                    flash(u'Unhandled database exception.', 'alert-danger')
                    return render_template('login.html', form=form, title="Login")

                flash(u'Login successful', 'alert-success')
                #return render_template('login.html', form=form, title="Login")
                #return redirect(url_for("session_test"))
                return render_template('profile.html', title="Profile")
            else:
                flash(u'This account has not been activated.', 'alert-danger')
                # return render_template('login.html', form=form, title="Login")
                form = ValidateEmailForm()
                session["validate_user_id"] = user.id

                return render_template('register.html',
                                       form=form,
                                       title="Activate",
                                       object="email",
                                       email=user.email)
        else:
            flash(u'Invalid credentials', 'alert-danger')
            return render_template('login.html', form=form, title="Login")
    else:
        # return "<h1>Error</h1>"
        # flash(u'Invalid credentials', 'alert-danger')
        return render_template('login.html', form=form, title="Login")


@app.route('/register/', methods=['GET', 'POST'])
def register():
    form = RegisterUserForm()

    if form.validate_on_submit():
        username = form.username.data.strip()
        email = form.email.data.strip()
        password = form.password.data.strip()
        hashed_password = generate_password_hash(password, method='sha256')
        level = 100
        token = s.dumps(form.email.data, salt=app.config['SALT'])

        #  Check for existence of username and email address.
        username_exists = User.query.filter(User.username == username).first()
        if username_exists:
            flash(u'Username already exists', 'alert-danger')
            return render_template('register.html', form=form, object="user", title="Register")

        email_exists = User.query.filter(User.email == email).first()
        if email_exists:
            flash(u'Email already exists', 'alert-danger')
            return render_template('register.html', form=form, object="user", title="Register")

        try:
            new_user = User(username=username,
                            email=email,
                            level=level,
                            password=hashed_password,
                            created_at=datetime.utcnow(),
                            verification_token=token
                            )
            db.session.add(new_user)
            db.session.commit()
        except exc.IntegrityError:
            flash(u'DB Integrity error.', 'alert-danger')  # Should never occur since we already check for dupes.
            return render_template('register.html', form=form, object="user", title="Register")
        except exc.OperationalError:
            flash(u'DB failure.', 'alert-danger')  # Is DB down?  Does table exist?
            return render_template('register.html', form=form, object="user", title="Register")
        except Exception as e:
            print(e)
            flash(u'Unhandled database exception.', 'alert-danger')
            return render_template('register.html', form=form, object="user", title="Register")

        send_verification_email(email, token)

        flash(u'User added', 'alert-success')
        return redirect((url_for("view_users")))
    else:
        # return "<h1>Error</h1>"
        return render_template('register.html', form=form, object="user", title="Register")


@app.route('/activate/', methods=['GET', 'POST'])
def activate():
    # Called if account tries to login and the email address was not yet activated.
    form = ValidateEmailForm()

    if form.validate_on_submit():
        my_id = session["validate_user_id"]
        email = form.email.data.strip()
        token = s.dumps(form.email.data, salt=app.config['SALT'])

        user = User.query.filter(User.id == my_id).first()

        # Make sure submitted email address does not belong to another user.
        if user.email == email:
            user.verification_token = token
            # print(token, len(token))
            db.session.commit()

            send_verification_email(email, token)

            flash(u'Please check your email for a verification link.', 'alert-success')
            return redirect((url_for("index")))
        else:
            email_exists = User.query.filter(User.email == email).first()

            if email_exists:    # This email already exists in the DB and is used by another user.  Show error.
                flash(u'Unable to use this email address (1).  Please submit another.', 'alert-danger')

                #form.email.data = email
                return render_template('register.html', title="Register", object="email", form=form, email=email)
            else:   # This email address does not exist in the DB.  Let this user register it.
                user.verification_token = token
                user.email = email
                # print(token, len(token))
                db.session.commit()

                send_verification_email(email, token)

                flash(u'Please check your email for a verification link.', 'alert-success')
                return redirect((url_for("index")))

    else:   # form errors
        return render_template('register.html',
                               form=form,
                               title="Activate",
                               object="email")


@app.route('/view_users', methods=['GET', 'POST'])
def view_users():
    form = UserSortForm()

    if request.method == 'POST':
        sort = form.sort_by.data
        if sort == "id":
            sort_by = "id"
            users = User.query.order_by(sort_by).all()
        elif sort == "id_d":
            sort_by = "id"
            users = User.query.order_by(getattr(User, sort_by).desc()).all()  # UGLY CODE!
        elif sort == "username":
            sort_by = "username"
            users = User.query.order_by(sort_by).all()
        elif sort == "username_d":
            sort_by = "username"
            users = User.query.order_by(getattr(User, sort_by).desc()).all()  # UGLY CODE!
        elif sort == "level":
            sort_by = "level"
            users = User.query.order_by(sort_by).all()
        elif sort == "level_d":
            sort_by = "level"
            users = User.query.order_by(getattr(User, sort_by).desc()).all()  # UGLY CODE!
        else:
            sort = "id"
            users = User.query.order_by(User.id.desc()).all()
    else:
        # Sort by newest first if sort option not submitted.
        users = User.query.order_by(User.id.desc()).all()
        #print(db.session.query)

    return render_template('view_items.html',
                           users=users,
                           form=form,
                           title="View Users",
                           object="users"
                           )


@app.route('/add-user/', methods=['GET', 'POST'])
def add_user():
    form = RegisterUserForm()

    if form.validate_on_submit():
        username = form.username.data.strip()
        email = form.email.data.strip()
        password = form.password.data.strip()
        hashed_password = generate_password_hash(password, method='sha256')
        level = 100
        token = s.dumps(form.email.data, salt=app.config['SALT'])

        #  Check for existence of username and email address.
        username_exists = User.query.filter(User.username == username).first()
        if username_exists:
            flash(u'Username already exists', 'alert-danger')
            return render_template('register.html', form=form, object="user", title="Register")

        email_exists = User.query.filter(User.email == email).first()
        if email_exists:
            flash(u'Email already exists', 'alert-danger')
            return render_template('register.html', form=form, object="user", title="Register")

        try:
            new_user = User(username=username,
                            email=email,
                            level=level,
                            password=hashed_password,
                            created_at=datetime.utcnow(),
                            verification_token=token
                            )
            db.session.add(new_user)
            db.session.commit()
        except exc.IntegrityError:
            flash(u'DB Integrity error.', 'alert-danger')  # Should never occur since we already check for dupes.
            return render_template('register.html', form=form, object="user", title="Register")
        except exc.OperationalError:
            flash(u'DB failure.', 'alert-danger')  # Is DB down?  Does table exist?
            return render_template('register.html', form=form, object="user", title="Register")
        except Exception as e:
            print(e)
            flash(u'Unhandled database exception.', 'alert-danger')
            return render_template('register.html', form=form, object="user", title="Register")

        send_verification_email(email, token)

        flash(u'User added', 'alert-success')
        return redirect((url_for("view_users")))
    else:
        # return "<h1>Error</h1>"
        return render_template('register.html', form=form, object="user", title="Register")


@app.route('/edit-user/<int:my_id>/', methods=['GET', 'POST'])
def edit_user(my_id):
    form = EditUserForm()
    user = User.query.filter(User.id == my_id).first()

    if user:
        if request.method == 'POST':
            if form.validate_on_submit():

                username = str(form.username.data.strip())
                email = str(form.email.data.strip())

                #  Check if another user already uses this username or email address.
                username_exists = User.query.filter(User.username == username).first()
                if username_exists:
                    if username_exists.id != my_id:
                        #print(username_exists.id, my_id)
                        flash(u'Username already exists.', 'alert-danger')
                        return render_template('edit_item.html', form=form, my_id=my_id, object="user")

                email_exists = User.query.filter(User.email == email).first()
                if email_exists:
                    if email_exists.id != my_id:
                        flash(u'Email already exists.', 'alert-danger')
                        return render_template('edit_item.html', form=form, my_id=my_id, object="user")

                # If we get to this point, username and email address are unique, so let's write to DB.

                try:
                    user.username = str(form.username.data.strip())
                    user.email = str(form.email.data.strip())
                    user.level = str(form.level.data.strip())

                    db.session.commit()

                    flash(u'User updated.', 'alert-success')
                    return redirect((url_for("view_users")))
                except exc.IntegrityError:
                    flash(u'DB Integrity error.',
                          'alert-danger')  # Should never occur since we already check for dupes.
                    return render_template('edit_item.html', form=form, my_id=my_id, object="user")
                except exc.OperationalError:
                    flash(u'DB failure.', 'alert-danger')  # Is DB down?  Does table exist?
                    return render_template('edit_item.html', form=form, my_id=my_id, object="user")
                except Exception as e:
                    print(e)
                    flash(u'Unhandled database exception.', 'alert-danger')
                    return render_template('edit_item.html', form=form, my_id=my_id, object="user")

            else:
                # print("update failed")

                #TODO remove
                #username = str(form.username.data.strip())
                #email = str(form.email.data.strip())
                #level = str(form.level.data.strip())

                return render_template('edit_item.html',
                                       my_id=my_id,
                                       form=form,
                                       object="user"
                                       )

        else:  # This is a GET, so display the edit form.
            username = user.username
            email = user.email
            level = user.level

            form.username.data = username
            form.email.data = email
            form.level.data = str(level)

            return render_template('edit_item.html',
                                   my_id=my_id,
                                   form=form,
                                   username=username,
                                   email=email,
                                   level=level,
                                   object="user"
                                   )
    else:
        flash(u'User not found', 'alert-danger')
        return redirect((url_for("view_users")))


@app.route('/delete-user/<int:my_id>/')
def delete_user(my_id):
    user = User.query.filter(User.id == my_id).first()

    if user:
        db.session.delete(user)
        db.session.commit()

        flash(u'User deleted.', 'alert-success')
        return redirect((url_for("view_users")))

    else:
        flash(u'User not found', 'alert-danger')
        return redirect((url_for("view_users")))


@app.route('/add-dog/', methods=['GET', 'POST'])
def add_dog():
    form = CreateDogForm()
    if form.validate_on_submit():
        name = form.name.data.capitalize().strip()
        age = form.age.data
        breed = form.breed.data.capitalize().strip()

        # Check for existence of name.  In the real world, it is OK to have
        # more than one dog with the same name but I am just demonstrating
        # a typical use case. - JG

        name_exists = Dog.query.filter(Dog.name == name).first()
        if name_exists:
            flash(u'A dog with this name already exists', 'alert-danger')
            return render_template('add_item.html', form=form, object="dog")

        # Dog name does not exist.  Add to the database.

        try:
            new_dog = Dog(name=name,
                            age=age,
                            breed=breed,
                            created_at=datetime.utcnow(),
                            )
            db.session.add(new_dog)
            db.session.commit()
        except exc.IntegrityError:
            flash(u'DB Integrity error.', 'alert-danger')  # Should never occur since we already check for dupes.
            return render_template('add_item.html', form=form, object="dog")
        except exc.OperationalError:
            flash(u'DB failure.', 'alert-danger')  # Is DB down?  Does table exist?
            return render_template('add_item.html', form=form, object="dog")
        except Exception as e:
            print(e)
            flash(u'Unhandled database exception.', 'alert-danger')
            return render_template('add_item.html', form=form, object="dog")

        flash(u'Dog added', 'alert-success')
        return redirect((url_for("view_dogs")))
    else:
        # return "<h1>Error</h1>"
        return render_template('add_item.html', form=form, object="dog")


@app.route('/view_dogs', methods=['GET', 'POST'])
def view_dogs():
    form = DogSortForm()

    if request.method == 'POST':
        sort = form.sort_by.data
        if sort == "id":
            sort_by = "id"
            dogs = Dog.query.order_by(sort_by).all()
        elif sort == "id_d":
            sort_by = "id"
            dogs = Dog.query.order_by(getattr(Dog, sort_by).desc()).all()  # UGLY CODE!
        elif sort == "name":
            sort_by = "name"
            dogs = Dog.query.order_by(sort_by).all()
        elif sort == "name_d":
            sort_by = "name"
            dogs = Dog.query.order_by(getattr(Dog, sort_by).desc()).all()  # UGLY CODE!
        elif sort == "age":
            sort_by = "age"
            dogs = Dog.query.order_by(sort_by).all()
        elif sort == "age_d":
            sort_by = "age"
            dogs = Dog.query.order_by(getattr(Dog, sort_by).desc()).all()  # UGLY CODE!
        elif sort == "breed":
            sort_by = "breed"
            dogs = Dog.query.order_by(sort_by).all()
        elif sort == "breed_d":
            sort_by = "breed"
            dogs = Dog.query.order_by(getattr(Dog, sort_by).desc()).all()  # UGLY CODE!

        else:
            sort = "id"
            dogs = Dog.query.order_by(Dog.id.desc()).all()
    else:
        # Sort by newest first if sort option not submitted.
        dogs = Dog.query.order_by(Dog.id.desc()).all()
        #print(db.session.query)

    return render_template('view_items.html',
                           dogs=dogs,
                           form=form,
                           title="View Dogs",
                           object="dogs"
                           )


@app.route('/edit-dog/<int:my_id>/', methods=['GET', 'POST'])
def edit_dog(my_id):
    form = EditDogForm()
    dog = Dog.query.filter(Dog.id == my_id).first()

    if dog:
        if request.method == 'POST':
            if form.validate_on_submit():

                name = str(form.name.data.strip().capitalize())
                breed = str(form.breed.data.strip().capitalize())
                age = form.age.data

                #  Check if another dog already uses this name.
                name_exists = Dog.query.filter(Dog.name == name).first()
                if name_exists:
                    if name_exists.id != my_id:
                        #print(username_exists.id, my_id)
                        flash(u'Dog already exists.', 'alert-danger')
                        return render_template('edit_item.html', form=form, my_id=my_id, object="dog")

                # If we get to this point, dog's name is unique, so let's write to DB.

                try:
                    dog.name = name
                    dog.age = age
                    dog.breed = breed

                    db.session.commit()

                    flash(u'Dog updated.', 'alert-success')
                    return redirect((url_for("view_dogs")))
                except exc.IntegrityError:
                    flash(u'DB Integrity error.',
                          'alert-danger')  # Should never occur since we already check for dupes.
                    return render_template('view_items.html', object="dogs")
                except exc.OperationalError:
                    flash(u'DB failure.', 'alert-danger')  # Is DB down?  Does table exist?
                    return render_template('view_items.html', object="dogs")
                except Exception as e:
                    print(e)
                    flash(u'Unhandled database exception.', 'alert-danger')
                    return render_template('view_items.html', object="dogs")

            else:
                # print("update failed")

                name = str(form.name.data.strip())
                breed = str(form.breed.data.strip())
                age = form.age.data

                return render_template('edit_item.html',
                                       my_id=my_id,
                                       form=form,
                                        object="dog"
                                       )

        else:  # This is a GET, so display the edit form.
            name = dog.name
            age = dog.age
            breed = dog.breed

            form.name.data = name
            form.age.data = age
            form.breed.data = breed

            return render_template('edit_item.html',
                                   my_id=my_id,
                                   form=form,
                                   name=name,
                                   age=age,
                                   breed=breed,
                                   object="dog"
                                   )
    else:
        flash(u'Dog not found', 'alert-danger')
        return redirect((url_for("view_dogs")))


@app.route('/delete-dog/<int:my_id>/')
def delete_dog(my_id):
    dog = Dog.query.filter(Dog.id == my_id).first()

    if dog:
        db.session.delete(dog)
        db.session.commit()

        flash(u'Dog deleted.', 'alert-success')
        return redirect((url_for("view_dogs")))

    else:
        flash(u'Dog not found', 'alert-danger')
        return redirect((url_for("view_dogs")))


@app.route('/session_test')
def session_test():
    #session["logged-in"] = True

    #return session_dump()
    return render_template('session_dump.html',
                           session_data=session_dump()
                           )


@app.route('/logout')
def logout():
    session.clear()

    flash(u'You have been logged out.', 'alert-success')
    return redirect(url_for('index'))


@app.route('/confirm-email/<token>/<my_email>', methods=['GET'])
def confirm_email(token, my_email):
    try:
        s.loads(token, salt=config.SALT, max_age=86400)  #86400=24 hours

        #  The token works.  Now verify it belongs to email address
        #  and update the relevant fields.

        user = User.query.filter(User.email == my_email).first()

        if user:
            user.active = True
            user.confirmed_at = datetime.utcnow()
            db.session.commit()

            flash(u'Activation successful!  Please login below.', 'alert-success')
            return redirect(url_for('login'))
        else:   # Email address does not exist.  Hacker?
            flash(u'Invalid email address.', 'alert-danger')
            return render_template('login.html', form=LoginForm())

    except SignatureExpired:
        flash(u'ERROR: Token has expired (1).  Try logging in again.', 'alert-danger')
        return render_template('login.html', form=LoginForm())
    except BadTimeSignature:
        flash(u'ERROR: Token is invalid (2).', 'alert-danger')
        return render_template('login.html', form=LoginForm())
    except BadSignature:
        flash(u'ERROR: Token is invalid (3).', 'alert-danger')
        return render_template('login.html', form=LoginForm())


@app.route('/profile/')
def profile():

    return render_template('profile.html', title="Profile")


@app.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    flash(u'Invalid URL', 'alert-warning')
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run()
