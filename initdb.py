from app import db
from app import User
from datetime import datetime

db.drop_all()
db.create_all()

user = User(username="joe1", email="joe1@joe.com", level=1, created_at=datetime.utcnow())

db.session.add(user)
db.session.commit()

print("DB initialized.")
