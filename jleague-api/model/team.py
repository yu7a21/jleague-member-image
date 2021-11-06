from config.db_config import db

class Team(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    short_name = db.Column(db.String(50), nullable=False)
    league = db.Column(db.String(50), nullable=False)