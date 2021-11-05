from flask import Flask
from config.db_config import init_db
from config import config
from model.team import Team

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = f"mysql://{config.db_user}:{config.db_password}@{config.db_host}/{config.db_database}?charset=utf8"
db = init_db(app)

@app.route('/hello')
def hello():
    result = Team.query.all()
    list = [t.name for t in result]
    return f"清水エスパルス：{list}"

if __name__ == '__main__':
    app.run(host="0.0.0.0", port="18070")