from src.player.repository.player_repository import PlayerRepository
from src.team.repository.team_repository import TeamRepository

class PlayerService():
    def __init__(self) -> None:
        self.player_repository = PlayerRepository()
        self.team_repository = TeamRepository()

    def find_all_by_team_id(self, team_id:int) -> list:
        """
        指定されたチームIDのチームに所属する選手を取得する

        :param team_id: チームID
        :type team_id: int
        :return: 選手リスト
        :rtype: list
        """
        #チームが存在するかチェック
        if self.team_repository.find_one_by_id(team_id) is None:
            return []

        return self.player_repository.find_all_by_team_id(team_id)


    def find_all_by_team_name(self, team_name:str) -> list:
        """
        指定されたチーム名のチームに所属する選手を取得する

        :param team_name: チーム名
        :type team_name: str
        :return: 選手リスト
        :rtype: list
        """
        #チームが存在するかチェック
        team = self.team_repository.find_one_by_name(team_name)
        if team is None:
            return []
        else:
            team_id = team.id
        return self.player_repository.find_all_by_team_id(team_id)