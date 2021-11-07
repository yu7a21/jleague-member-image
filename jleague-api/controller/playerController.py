from http import HTTPStatus
import json

from model.player import Player
from model.team import Team
from error import response_error

def player(team_id, team_name):
    player = Player()
    if team_id:
        query_results = player.query.filter_by(team_id=team_id).all()
        if len(query_results) == 0:
            return response_error(f"指定されたチームIDのチームは存在しません 指定されたID:{team_id}", HTTPStatus.BAD_REQUEST)
    elif team_name:
        team = Team()
        team_by_id = team.query.filter_by(name=team_name).first()
        if team_by_id is None:
            return response_error(f"指定されたチーム名のチームは存在しません 指定されたチーム名:{team_name}", HTTPStatus.BAD_REQUEST)
        query_results = player.query.filter_by(team_id=team_by_id.team_id).all()
    ret = []
    for result in query_results:
        ret.append({
            "id":result.id,
            "name_ja":result.name_ja,
            "name_en":result.name_en,
            "number":result.number,
            "team_id":result.team_id
        })
    return json.dumps(ret, ensure_ascii=False, indent=4)