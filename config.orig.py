SECRET_KEY = b'SET_YOUR_OWN_KEY_HERE'

# See freemysqlhosting.net for free mySQL.
DB_USERNAME = "name"
DB_PASSWORD = "pass"
DB_HOST     = "db_host"
DB_DATABASE = "db_name"

SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://{}:{}@{}/{}"\
.format(DB_USERNAME, DB_PASSWORD, DB_HOST, DB_DATABASE)

SQLALCHEMY_POOL_RECYCLE = 280   # See http://help.pythonanywhere.com/pages/UsingSQLAlchemywithMySQL/
SQLALCHEMY_TRACK_MODIFICATIONS = True
#SQLALCHEMY_ECHO = True

# MAIL SETTINGS
# See postale.io for free email hosting.
#POSTALE SETTINGS
MAIL_SERVER = "mail.postale.io"
MAIL_USERNAME = "a@b.com"
MAIL_SENDER = "My name <a@b.com>"
MAIL_PASSWORD = "your_password"
MAIL_PORT = 587
MAIL_USE_SSL = False
MAIL_USE_TLS = True
MAIL_DEBUG = 0

# SALT FOR EMAIL CONFIRMATION - FUTURE USE
SALT = "FUTURE_USE"

# FOR EMAIL CONFIRMATION
ROOT_URL = "http://127.0.0.1:5000"

# USED FOR GOOGLE ANALYTICS.  IF NOT PRODUCTION, DO NOT INCLUDE THE TRACKING SCRIPT. - FUTURE USE
# TESTING = True

IS_PRODUCTION = False

# RECAPTCHA KEYS - DIFFERENT KEYS FOR DEV AND PROD
RECAPTCHA_PUBLIC_KEY_DEV = "A"
RECAPTCHA_PRIVATE_KEY_DEV = "B"

RECAPTCHA_PUBLIC_KEY_PROD = "C"
RECAPTCHA_PRIVATE_KEY_PROD = "D"