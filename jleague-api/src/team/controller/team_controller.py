from http import HTTPStatus

from error import response_error

from src.team.service.team_service import TeamService

def team(team_id:int) -> dict:
    """
    チーム情報を返却する

    :param team_id: チームID。空だったら全チーム分返却する
    :type team_id: int
    :return: チーム情報
    :rtype: dict
    """
    team_service = TeamService()
    if team_id:
        team = team_service.find_one_by_id(team_id)
        if team is None:
            return response_error(f"指定されたチームIDのチームは存在しません 指定されたID:{team_id}", HTTPStatus.BAD_REQUEST)
        team_list = [team]
    else:
        team_list = team_service.find_all()

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
