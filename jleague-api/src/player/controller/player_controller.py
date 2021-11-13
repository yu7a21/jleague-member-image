from http import HTTPStatus

from src.player.service.player_service import PlayerService

from src.utils.error import response_error
from src.utils.error import TeamNotFoundException
from src.utils.error import PlayerNotFoundException

def player(team_id:int, team_name:str) -> dict:
    """
    選手情報を返却する

    :param team_id: チームID
    :type team_id: int
    :param team_name: チーム名
    :type team_name: str
    :return: 選手情報
    :rtype: dict
    """
    player_service = PlayerService()
    try:
        if team_id:
            players_list = player_service.find_all_by_team_id(team_id)
        elif team_name:
            players_list = player_service.find_all_by_team_name(team_name)
    except (PlayerNotFoundException, TeamNotFoundException) as e:
        return response_error(e.message, e.status)
    except Exception as e:
        return response_error(e, HTTPStatus.INTERNAL_SERVER_ERROR)

    ret = {}
    for result in players_list:
        if result.team_id not in ret:
            ret[result.team_id] = []
        ret[result.team_id].append({
            "id":result.id,
            "name_ja":result.name_ja,
            "name_en":result.name_en,
            "number":result.number,
            "team_id":result.team_id
        })
    return ret