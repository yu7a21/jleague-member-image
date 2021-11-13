from flask_sqlalchemy import SQLAlchemy

from config import config

db = SQLAlchemy()

def init_db(flask_app):
    flask_app.config["SQLALCHEMY_DATABASE_URI"] = f"mysql://{config.DB_USER}:{config.DB_PASSWORD}@{config.DB_HOST}/{config.DB_DATABASE}?charset=utf8"
    db.init_app(flask_app)