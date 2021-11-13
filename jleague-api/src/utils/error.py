from http import HTTPStatus

def response_error(message:str, status:int) -> tuple:
    """
    エラーレスポンス組み立て

    :param message: エラーメッセージ
    :type message: [type]
    :param status: ステータスコード
    :type status: [type]
    :return: エラーレスポンス
    :rtype: [type]
    """
    return {"meesage":message, "status":status}, status

class TeamNotFoundException(Exception):
    def __init__(self, message):
        self.message = f"【TeamNotFoundException】 {message}"
        self.status = HTTPStatus.BAD_REQUEST

class PlayerNotFoundException(Exception):
    def __init__(self, message):
        self.message = f"【PlayerNotFoundException】 {message}"
        self.status = HTTPStatus.BAD_REQUEST