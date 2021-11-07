from config.db_config import db

class Player(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name_ja = db.Column(db.String(100), nullable=False)
    name_en = db.Column(db.String(100), nullable=False)
    number = db.Column(db.Integer, nullable=True)
    team_id = db.Column(db.Integer, nullable=False)