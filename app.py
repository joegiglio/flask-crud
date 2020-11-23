# Flask-Mail reference: https://www.youtube.com/watch?v=vF9n248M1yk

from flask import Flask, render_template, redirect, url_for, request, flash, session, render_template_string
from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField, PasswordField, BooleanField, TextAreaField, SelectField, HiddenField, IntegerField
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms.validators import InputRequired, Email, Length, NumberRange, EqualTo, Regexp, DataRequired
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import exc, func, MetaData
from utils import session_dump
from flask_migrate import Migrate


# Unused but may need them later!
#from werkzeug.security import generate_password_hash, check_password_hash
#from datetime import datetime
#from itsdangerous import URLSafeTimedSerializer, SignatureExpired, BadTimeSignature
#from utils import session_dump, is_user_admin
#from decorators import session_required, admin_required, session_required_obj, session_required_review
#from strings import companies_snippet
#from flask_mail import Mail, Message


app = Flask(__name__)
app.config.from_pyfile("config.py")
#mail = Mail(app)

#s = URLSafeTimedSerializer(app.config['SECRET_KEY'])
db = SQLAlchemy(app)
migrate = Migrate(app, db)


#   TODO: Move models to separate file.  I was having inheritace issues with db.create_all.  Need to revisit.

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
                               InputRequired(),
                               Length(message="Username must be between 4 and 20 characters",
                                      min=4, max=20)
                           ])
    password = PasswordField('Password', validators=[
                                InputRequired(),
                                Length(message="Password must be between 8 and 80 characters.",
                                       min=8, max=80)])
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
    #password = db.Column(db.String(255), nullable=False, server_default='')
    #active = db.Column(db.Boolean(), nullable=False, server_default='0')
    email = db.Column(db.String(255), nullable=False, unique=True)
    #verification_token = db.Column(db.String(50), nullable=False)
    #pw_reset_token = db.Column(db.String(50))
    #confirmed_at = db.Column(db.DateTime())
    #login_count = db.Column(db.Integer, server_default='0')
    #last_active = db.Column(db.DateTime())
    #notification_optin = db.Column(db.Boolean, server_default='1', default=True)
    level = db.Column(db.Integer)


class Dog(db.Model):
    # __table_args__ = {'sqlite_autoincrement': True}
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime())
    name = db.Column(db.String(20), nullable=False, unique=True)
    age = db.Column(db.Integer)
    breed = db.Column(db.String(20), nullable=False)


@app.route('/', methods=['GET', 'POST'])
def index():
    form = SampleForm()

    if form.validate_on_submit():
        print("yes")
    else:
        print("no")

    return render_template('index.html',
                           form=form,
                           initials="jg",
                           username=form.username.data
                           )


@app.route('/add-user/', methods=['GET', 'POST'])
def add_user():
    form = CreateUserForm()

    if form.validate_on_submit():
        username = form.username.data.strip()
        email = form.email.data.strip()
        level = form.level.data.strip()

        #  Check for existence of username and email address.
        username_exists = User.query.filter(User.username == username).first()
        if username_exists:
            flash(u'Username already exists', 'alert-danger')
            return render_template('add_item.html', form=form, object="user", title="Add User")

        email_exists = User.query.filter(User.email == email).first()
        if email_exists:
            flash(u'Email already exists', 'alert-danger')
            return render_template('add_item.html', form=form, object="user", title="Add User")

        try:
            new_user = User(username=username,
                            email=email,
                            level=level,
                            created_at=datetime.utcnow(),
                            )
            db.session.add(new_user)
            db.session.commit()
        except exc.IntegrityError:
            flash(u'DB Integrity error.', 'alert-danger')  # Should never occur since we already check for dupes.
            return render_template('add_item.html', form=form, object="user", title="Add User")
        except exc.OperationalError:
            flash(u'DB failure.', 'alert-danger')  # Is DB down?  Does table exist?
            return render_template('add_item.html', form=form, object="user", title="Add User")
        except Exception as e:
            print(e)
            flash(u'Unhandled database exception.', 'alert-danger')
            return render_template('add_item.html', form=form, object="user", title="Add User")

        flash(u'User added', 'alert-success')
        return redirect((url_for("view_users")))
    else:
        # return "<h1>Error</h1>"
        return render_template('add_item.html', form=form, object="user", title="Add User")


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
                        return render_template('edituser.html', form=form, my_id=my_id)

                email_exists = User.query.filter(User.email == email).first()
                if email_exists:
                    if email_exists.id != my_id:
                        flash(u'Email already exists.', 'alert-danger')
                        return render_template('edituser.html', form=form, my_id=my_id)

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
                    return render_template('adduser.html')
                except exc.OperationalError:
                    flash(u'DB failure.', 'alert-danger')  # Is DB down?  Does table exist?
                    return render_template('adduser.html')
                except Exception as e:
                    print(e)
                    flash(u'Unhandled database exception.', 'alert-danger')
                    return render_template('adduser.html')

            else:
                # print("update failed")

                username = str(form.username.data.strip())
                email = str(form.email.data.strip())
                level = str(form.level.data.strip())

                return render_template('edituser.html',
                                       my_id=my_id,
                                       form=form
                                       )

        else:  # This is a GET, so display the edit form.
            username = user.username
            email = user.email
            level = user.level

            form.username.data = username
            form.email.data = email
            form.level.data = str(level)

            return render_template('edituser.html',
                                   my_id=my_id,
                                   form=form,
                                   username=username,
                                   email=email,
                                   level=level
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


@app.route('/session_test')
def session_test():
    #session["logged-in"] = True

    return session_dump()


@app.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    flash(u'Invalid URL', 'alert-warning')
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run()
