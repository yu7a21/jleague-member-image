from src.team.model.team import Team

class TeamRepository():
    def __init__(self):
        self.team = Team()

    def find_all(self) -> list:
        """
        全チーム情報を取得する

        :return: チーム情報
        :rtype: list
        """
        return self.team.query.all()

    def find_one_by_id(self, id:int) -> Team or None:
        """
        チームをIDで検索する

        :param id: チームID
        :type id: int
        :return: チーム情報。ヒットしなかったらNoneを返す
        :rtype: Team or None
        """
        return self.team.query.filter_by(id=id).one_or_none()

    def find_one_by_name(self, name:str) -> Team or None:
        """
        チームを名前で検索する

        :param name: チーム名
        :type name: str
        :return: チーム情報。ヒットしなかったらNoneを返す
        :rtype: Team or None
        """
        return self.team.query.filter_by(name=name).one_or_none()