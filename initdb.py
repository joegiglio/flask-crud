import os
from app import db
from flask import Flask
from app import User
from app import Dog
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import datetime
from werkzeug.security import generate_password_hash

app = Flask(__name__)
#db = SQLAlchemy(app)
migrate = Migrate(app, db)

print("Running Flask-Migrate scripts...")

os.system("flask db init")  # creates migrations directory
os.system('flask db migrate -m "Initial migration."')  # creates migration files
os.system("flask db upgrade")  # applies DB change

print("Creating sample data...")

hashed_password = generate_password_hash("joetest", method='sha256')
user = User(username="joetest", email="joe+test@joegiglio.org", level=100, created_at=datetime.utcnow(),
            verification_token="null", active=1, password=hashed_password)

hashed_password = generate_password_hash("password", method='sha256')
superadmin = User(username="superadmin", email="joe+superadmin@joegiglio.org", level=300, created_at=datetime.utcnow(),
                  verification_token="null", active=1, password=hashed_password)

dog = Dog(name="Romeo", breed="Maltese", age=12, created_at=datetime.utcnow())

db.session.add(user)
db.session.add(superadmin)
db.session.add(dog)
db.session.commit()

print("Database initialized.")
