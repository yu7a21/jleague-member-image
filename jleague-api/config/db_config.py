from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def init_db(flask_app):
    db.init_app(flask_app)