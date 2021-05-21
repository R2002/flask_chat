from database import db

class Chat(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(20))
    name = db.Column(db.String(20))
    icon = db.Column(db.String(100))
    color = db.Column(db.String(10))
    time = db.Column(db.Integer)
    comment = db.Column(db.String(100))
