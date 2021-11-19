from http import HTTPStatus
from flask import Flask, request
import json

from config.db_config import init_db
from src.utils.error import response_error

from src.generate_image.controller.generate_image_controller import generate_image
from src.player.controller.player_controller import player
from src.team.controller.team_controller import team

app = Flask(__name__)
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
        return response_error("チームIDもしくはチーム名どちらか片方のみ、必ず指定してください", HTTPStatus.BAD_REQUEST)
    if not str.isdigit(team_id) and team_id != "":
        return response_error("チームIDに数字以外が設定されています", HTTPStatus.BAD_REQUEST)

    return player(team_id, team_name)

#TODO:フロントできたらPOST指定する
@app.route('/generate_image')
def generate_images():
    req_json = request.json
    if req_json is None:
        #TODO:フロントが動くようになったら消す
        return generate_image()
        return response_error("画像生成用のデータがありません", HTTPStatus.BAD_REQUEST)
    else:
        req_dict = json.loads(req_json)
        #TODO:中身のチェック、せめてkeyくらいは
        return generate_image(req_dict["image_info"], req_dict["position_data"])

def is_empty_str(str:str):
    return str == ""

if __name__ == '__main__':
    app.run(host="0.0.0.0", port="18070")