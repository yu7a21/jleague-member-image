from http import HTTPStatus
import json

from model.team import Team
from error import response_error

def team(team_id):
    team = Team()
    if team_id:
        query_results = team.query.filter_by(id=team_id).all()
        if len(query_results) == 0:
            return response_error(f"指定されたチームIDのチームは存在しません 指定されたID:{team_id}", HTTPStatus.BAD_REQUEST)
    else:
        query_results = team.query.all()
    dict = {}
    for result in query_results:
        dict[result.name] = {
            "id":result.id,
            "short_name":result.short_name,
            "league":result.league,
            "color":result.color
        }
    return json.dumps(dict, ensure_ascii=False, indent=4)
