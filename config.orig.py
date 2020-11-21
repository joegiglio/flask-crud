SQLALCHEMY_DATABASE_URI = 'sqlite:////Users/joe/Documents/programming/python/rs1/Remote-Scorecard/database.db'
SQLALCHEMY_POOL_RECYCLE = 280   # See http://help.pythonanywhere.com/pages/UsingSQLAlchemywithMySQL/

SECRET_KEY = b'\xe2\xd4\x94$\xcc*\xb12\xf9\xdb\xbd\x1cv\xc6\'\xf1\x18\x92\x0c\xe6\xbb\xb93\x07"i\x93\x17\x82a\xe4\xbe'
#SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://cdenninger:Sc0r3f0rce!@aar9uh48ns0okt.ccy0cyau8b1c.us-west-2.rds.amazonaws.com/rs_db"

#PYTHONANYWHERE CONFIG:
#SQLALCHEMY_DATABASE_URI = "mysql://joeg:Corona-seattle@joeg.mysql.pythonanywhere-services.com/joeg$rs"

# MAIL SETTINGS
#POSTALE SETTINGS
MAIL_SERVER = "mail.postale.io"
MAIL_USERNAME = "support@remotescorecard.com"
MAIL_SENDER = "RemoteScorecard.com Support <support@remotescorecard.com>"
MAIL_PASSWORD = "Postale9440!"
MAIL_PORT = 587
MAIL_USE_SSL = False
MAIL_USE_TLS = True
MAIL_DEBUG = 0

# SALT FOR EMAIL CONFIRMATION
SALT = b'%;\xc9h\xe5\x8b\xb3\xffH\x9dK\r\x139\x172w\x9a\xcat\xbeV|\\@nx8\x18\xcdDa"3i\xef'

# FLASK-USER SETTINGS
CSRF_ENABLED = True
USER_ENABLE_EMAIL = True
USER_APP_NAME = "V2"

# FOR EMAIL CONFIRMATION
ROOT_URL = "http://127.0.0.1:5000"

# PATH FOR FILE UPLOADS
UPLOAD_FOLDER = '/Users/joe/Documents/programming/python/rs1/Remote-Scorecard/static/images/uploads/'

# MAX FILE UPLOAD SIZE
MAX_CONTENT_LENGTH = 2 * 1024 * 1024    # 2MB.  This might have some side effects but I can't find a better server side option.
                                        # - JG, 4/13/20

# USED FOR GOOGLE ANALYTICS.  IF NOT PRODUCTION, DO NOT INCLUDE THE TRACKING SCRIPT.
IS_PRODUCTION = False

# RECAPTCHA KEYS - DIFFERENT KEYS FOR DEV AND PROD
RECAPTCHA_PUBLIC_KEY_DEV = "6LfWzPUUAAAAAFieJ1lCEZEoebP-ANgxx_SUjLGL"
RECAPTCHA_PRIVATE_KEY_DEV = "6LfWzPUUAAAAADeQs4fZjgq5UDuObg-ZjX7M7Puc"
#TESTING = True
RECAPTCHA_PUBLIC_KEY_PROD = "6LeBzPUUAAAAAF0v9aOf3l8sWdi0SJ_CZ42nZ0Vn"
RECAPTCHA_PRIVATE_KEY_PROD = "6LeBzPUUAAAAAD5urASZ2eobdFDkHdx_-q79jZY_"