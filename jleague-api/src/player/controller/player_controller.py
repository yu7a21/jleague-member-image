from http import HTTPStatus

from error import response_error

from src.player.service.player_service import PlayerService

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
    if team_id:
        players_list = player_service.find_all_by_team_id(team_id)
        #TODO:チームの存在チェックとエラーハンドリングはserviceでやる
        if len(players_list) == 0:
            return response_error(f"指定されたチームIDのチームは存在しないか、選手が一人も登録されていません。 指定されたID:{team_id}", HTTPStatus.BAD_REQUEST)
    elif team_name:
        players_list = player_service.find_all_by_team_name(team_name)

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