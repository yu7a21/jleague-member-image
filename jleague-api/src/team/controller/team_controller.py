from http import HTTPStatus

from src.team.service.team_service import TeamService

from src.utils.error import response_error
from src.utils.error import TeamNotFoundException
from src.utils.error import PlayerNotFoundException

def team(team_id:int) -> dict:
    """
    チーム情報を返却する

    :param team_id: チームID。空だったら全チーム分返却する
    :type team_id: int
    :return: チーム情報
    :rtype: dict
    """
    team_service = TeamService()
    try:
        if team_id:
            team_list = [team_service.find_one_by_id(team_id)]
        else:
            team_list = team_service.find_all()
    except PlayerNotFoundException as e:
        return response_error(e.message, e.status)
    except TeamNotFoundException as e:
        return response_error(e.message, e.status)
    except Exception as e:
        return response_error(e, HTTPStatus.INTERNAL_SERVER_ERROR)

    dict = {}
    for result in team_list:
        dict[result.id] = {
            "id":result.id,
            "name":result.name,
            "short_name":result.short_name,
            "league":result.league,
            "color":result.color
        }
    return dict
