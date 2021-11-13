#選択されたチームのIDとフォーメーション(これはmock。ほんとはフロントからjsonで送られてくる)
mock_image_info = {
    "team_id":7,
    "formation":"4-4-2"
}

#ポジションと選手の対応データ(これはmock。ほんとはフロントからjsonで送られてくる)
mock_position_data = {
    "RCF":9, #サンタナ
    "LCF":24, #藤本
    "RW":7, #片山
    "RCM":33, #松岡
    "LCM":3, #ホナウド
    "LW":16, #西澤
    "RSB":18, #エウシーニョ
    "RCB":50, #鈴木
    "LCB":2, #立田
    "LSB":4, #原
    "GK":37 #権田
}
from src.generate_image.service.generate_image_service import GenerateImageService

def generate_image(image_info:dict = mock_image_info, position_data:dict = mock_position_data) -> dict:
    """
    スタメン画像のパスを返却する

    :param image_info: フロントから送られてくる画像生成に必要なデータ, defaults to mock_image_info
    :type image_info: dict, optional
    :param position_data: フロントから送られてくるポジションデータ, defaults to mock_position_data
    :type position_data: dict, optional
    :return: 画像へのパス
    :rtype: dict
    """
    generate_image_service = GenerateImageService(image_info, position_data)

    #先に画像色をチームカラーに置換
    generate_image_service.change_uniform_color()

    #背番号を全選手分いれる
    generate_image_service.write_number_to_uniform_image()

    #ユニ画像・名前文字列の入った画像を作成
    formation_image_path = generate_image_service.write_uniform_and_name_to_formation_image()

    #後片付け
    generate_image_service.clean_up_resources()

    return {"image_path":formation_image_path}