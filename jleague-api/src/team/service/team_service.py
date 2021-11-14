from src.team.model.team import Team
from src.team.repository.team_repository import TeamRepository

class TeamService():
    def __init__(self) -> None:
        self.team_repository = TeamRepository()

    def find_one_by_id(self, id:int) -> Team:
        """
        チーム情報をIDで取得する

        :param id: チームID
        :type id: int
        :return: 取得したチーム情報
        :rtype: Team
        """
        #チームが存在するかチェック
        return self.team_repository.find_one_by_id(id)

    def find_all(self) -> list:
        """
        DBに保存されている全チーム情報を取得する

        :return: チーム情報
        :rtype: list
        """
        return self.team_repository.find_all()