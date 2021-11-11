from http import HTTPStatus
from flask import Flask, Response, request
import json

from config.db_config import init_db
from config import config
from error import response_error
from controller.teamController import team
from controller.playerController import player
from controller.generateImageController import generate_image

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = f"mysql://{config.db_user}:{config.db_password}@{config.db_host}/{config.db_database}?charset=utf8"
db = init_db(app)

@app.route('/')
def index():
    return "Hello"

@app.route('/teams')
def teams():
    team_id = request.args.get("team_id", "")
    if not str.isdigit(team_id) and team_id != "":
        return response_error("チームIDに数字以外が設定されています", HTTPStatus.BAD_REQUEST)
    return team(team_id)

@app.route('/players')
def players():
    team_id = request.args.get("team_id", "")
    team_name = request.args.get("team_name", "")

    if not (is_empty_str(team_id) ^ is_empty_str(team_name)):
        return response_error("チームIDもしくはチーム名どちらか片方のみを必ず指定してください", HTTPStatus.BAD_REQUEST)
    if not str.isdigit(team_id) and team_id != "":
        return response_error("チームIDに数字以外が設定されています", HTTPStatus.BAD_REQUEST)

    return player(team_id, team_name)

@app.route('/generate_image')
def generate_images():
    return generate_image()

def is_empty_str(str:str):
    return str == ""

if __name__ == '__main__':
    app.run(host="0.0.0.0", port="18070")