from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# DB規定
db = SQLAlchemy()

# db初期設定
def init_database(app):
    db.init_app(app)
    Migrate(app, db)

def db_insert(data):
    db.session.add(data)
    db.session.commit()

def db_delete(data):
    db.session.delete(data)
    db.session.commit()