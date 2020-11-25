import os
from app import db
from flask import Flask
from app import User
from app import Dog
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import datetime

app = Flask(__name__)
#db = SQLAlchemy(app)
migrate = Migrate(app, db)

print("Running Flask-Migrate scripts...")

os.system("flask db init")  # creates migrations directory
os.system('flask db migrate -m "Initial migration."')  # creates migration files
os.system("flask db upgrade")  # applies DB change

print("Creating sample data...")

user = User(username="joe1", email="joe1@joe.com", level=100, created_at=datetime.utcnow())
dog = Dog(name="Romeo", breed="Maltese", age=12, created_at=datetime.utcnow())

db.session.add(user)
db.session.add(dog)
db.session.commit()

print("Database initialized.")
