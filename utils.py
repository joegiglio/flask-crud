from flask import session

from flask import Flask
from flask_mail import Mail, Message

app = Flask(__name__)
application = app

app.config.from_pyfile("config.py")

mail = Mail(app)


def session_dump():
    session_data = ""

    for key, value in session.items():
        session_data = session_data + str(key) + ": " + str(value) + "<br>"

    return str(session_data)


def is_user_admin():
    if ("user_level" in session) and (session["user_level"] == 200):
        return True
    else:
        return False


def is_user_super_admin():
    if ("user_level" in session) and (session["user_level"] == 300):
        return True
    else:
        return False


# def send_verification_email(my_token, my_email):
#
#     subject = "Test Subject from Flask app"
#     email_body = """Thank you for registering.<br>
#         Click this link to verify your address: <a href='{}/confirm-email/{}/{}'>Verify email</a>"""\
#         .format(app.config['ROOT_URL'], my_token, my_email)
#
#     msg = Message(subject=subject, sender=app.config['MAIL_SENDER'],
#                   recipients=[my_email], html=email_body)
#
#     mail.send(msg)


def send_verification_email(my_email, my_token):

    subject = "Test Subject from Flask app"
    email_body = """Thank you for registering.<br>
        Click this link to verify your email address: <a href='{}/confirm-email/{}/{}'>Verify email</a>"""\
        .format(app.config['ROOT_URL'], my_token, my_email)

    msg = Message(subject=subject, sender=app.config['MAIL_SENDER'],
                  recipients=[my_email], html=email_body)

    mail.send(msg)


def send_webform_email(my_to, my_subject, my_body):

    my_body_fix_linebreaks = my_body.replace("\n", "<br>")

    msg = Message(subject=my_subject, sender=app.config['MAIL_SENDER'],
                  recipients=[my_to], html=my_body_fix_linebreaks)

    mail.send(msg)
