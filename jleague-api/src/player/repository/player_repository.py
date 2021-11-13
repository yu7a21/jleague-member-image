from src.player.model.player import Player

class PlayerRepository():
    def __init__(self):
        self.player = Player()

    def find_all_by_team_id(self, team_id:int) -> list:
        """
        選手をチームIDで検索

        :param team_id: チームID
        :type team_id: int
        :return: 指定されたチームに所属する選手情報
        :rtype: list
        """
        return self.player.query.filter_by(team_id=team_id).all()

    def find_one_by_team_id_and_number(self, team_id:int, number:int) -> Player or None:
        """
        選手をチーム名と背番号で検索

        :param team_id: チームID
        :type team_id: int
        :param number: 背番号
        :type number: int
        :return: 指定されたチームの指定された背番号の選手情報。該当データがなかったらNoneを返す。
        :rtype: Player or None
        """
        return self.player.query.filter_by(team_id=team_id, number=number).one_or_none()