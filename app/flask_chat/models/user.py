from database import db
from flask_login import UserMixin

class User(db.Model, UserMixin):
    id = db.Column(db.String(20), primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(20))
    icon = db.Column(db.String(100))
    color = db.Column(db.String(10))
