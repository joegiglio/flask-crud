from flask import Flask
from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField, PasswordField, BooleanField, TextAreaField, SelectField, HiddenField
from wtforms.validators import InputRequired, Email, Length, EqualTo, Regexp, DataRequired
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import exc, func, MetaData

from flask_wtf.file import FileField, FileAllowed, FileRequired

app = Flask(__name__)
app.config.from_pyfile("config.py")
db = SQLAlchemy(app)

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
    #ip_address = db.Column(db.String(30), nullable=False)
    #last_active = db.Column(db.DateTime())
    #notification_optin = db.Column(db.Boolean, server_default='1', default=True)
    level = db.Column(db.Integer, server_default='1')
