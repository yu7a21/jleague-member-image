#https://hashikake.com/Pillow
from PIL import Image, ImageDraw, ImageFont, ImageChops
import os, shutil
from model.player import Player
from model.team import Team
from config import config

#各フォーメーションごと、ポジションの座標データ
#座標取得:http://wisteriahill.sakura.ne.jp/OpenCV/getArea4Haartraining/
mock_position_position_data = {
    "4-4-2":{
        "RCF": (290,260),
        "LCF": (290,462),
        "RW": (536,96),
        "RCM": (536,260),
        "LCM": (536,462),
        "LW": (536,632),
        "RSB": (801,96),
        "RCB": (801,260),
        "LCB": (801,462),
        "LSB": (801,632),
        "GK": (1010,378),
    },
    "4-3-3":{
        "RST": (),
        "CF": (),
        "LST": (),
        "RW": (),
        "CM": (),
        "LW": (),
        "RSB": (801,96),
        "RCB": (801,260),
        "LCB": (801,462),
        "LSB": (801,632),
        "GK": (1027,378),
    }
}
class GenerateImageService():
    def __init__(self, image_info:dict, position_data:dict):
        self.position_data = position_data

        self.team_id = image_info["team_id"]
        self.formation = image_info["formation"]

        #TODO:DBを見る処理はmodelにかくべき
        self.color_list = Team.query.filter_by(id=image_info["team_id"]).first().color.split(",")
        self.team_color = (int(self.color_list[0]), int(self.color_list[1]), int(self.color_list[2]))

    def change_uniform_color(self):
        """
        デフォルトのユニフォーム画像（白）をチームカラーで置換する。処理内容:https://qiita.com/pashango2/items/d6dda5f07109ee5b6163

        """
        uniform_img = Image.open(self.get_resolve_path(config.DEFAULT_UNIFORM_IMAGE_PATH))
        default_color = (255,255,255)
        #aないと怒られる
        r, g, b, a = uniform_img.split()

        _r = r.point(lambda _: 1 if _ == default_color[0] else 0, mode="1")
        _g = g.point(lambda _: 1 if _ == default_color[1] else 0, mode="1")
        _b = b.point(lambda _: 1 if _ == default_color[2] else 0, mode="1")

        mask = ImageChops.logical_and(_r, _g)
        mask = ImageChops.logical_and(mask, _b)

        uniform_img.paste(Image.new("RGB", uniform_img.size, self.team_color), mask=mask)
        uniform_img.save(self.get_resolve_path(config.TEAM_COLOR_UNIFORM_PATH))

    def write_number_to_uniform_image(self):
        """
        11人分の背番号入りユニ画像を作成
        """
        if not os.path.exists(self.get_resolve_path(config.PLAYER_UNIFORM_FOLDER_PATH)):
            os.mkdir(self.get_resolve_path(config.PLAYER_UNIFORM_FOLDER_PATH))
        for number in self.position_data.values():
            self.generate_uniform_image(str(number))

    def write_uniform_and_name_to_formation_image(self):
        """
        全選手のユニ画像・名前が入ったスタメン画像を作成
        """

        #先にピッチ画像をコピーしておく
        Image.open(self.get_resolve_path(config.INIT_FIELD_IMAGE_PATH)).copy().save(self.get_resolve_path(config.FORMATION_IMAGE_PATH))

        #背番号とポジションの対応を見て各ポジションにユニ画像・名前文字列を配置
        #TODO:攻撃方向を示す矢印とかおいた方がいいかも
        for position, number in self.position_data.items():
            self.generate_formation_image(position, str(number))

    def clean_up_resources(self):
        """
        今回の処理で作られたユニ画像を削除
        """
        #全選手分作ったユニを削除
        shutil.rmtree(self.get_resolve_path(config.PLAYER_UNIFORM_FOLDER_PATH))

        #色変更した画像削除
        os.remove(self.get_resolve_path(config.TEAM_COLOR_UNIFORM_PATH))

    def generate_uniform_image(self, number:str):
        """
        ユニフォーム画像に背番号を入れ背番号の入ったファイル名で保存する

        :param number: 入れる背番号
        :type number: str
        """
        uniform_img = Image.open(self.get_resolve_path(config.TEAM_COLOR_UNIFORM_PATH))
        #描画開始
        draw = ImageDraw.Draw(uniform_img)
        #フォント読み込み
        font = ImageFont.truetype(self.get_resolve_path(config.FONT_PATH), config.UNIFORM_NUMBER_FONT_SIZE)
        #文字描画(anchorは指定座標が文字エリアのどこにくるかの設定。この場合中央)
        draw.text(config.UNIFORM_NUMBER_POSITION, number, font=font, fill="black", align="center", anchor="mm")
        #画像保存
        uniform_img.save(self.get_resolve_path(f"{config.PLAYER_UNIFORM_FOLDER_PATH}/uniform_{number}.png"))

    #TODO:もっと分割できそう
    def generate_formation_image(self, position_name:str, number:str):
        """引数で指定された背番号の選手のユニ画像・選手名をフォーメーション画像に描画する

        :param formation: フォーメーション(ex:4-4-2)
        :type formation: str
        :param team_id: チームID
        :type team_id: int
        :param position_name: 選手のポジション名(ex:CF)
        :type position_name: str
        :param number: 選手の背番号
        :type number: str
        """
        #TODO:英語名と日本語名選べるようにする？
        player_name = Player.query.filter_by(team_id=self.team_id, number=number).first().name_ja

        #各ポジションのピッチ画像上の座標（左上がこの座標にあう）https://note.nkmk.me/python-pillow-paste/
        player_image_position = mock_position_position_data[self.formation][position_name]

        #ユニ画像を小さくリサイズして取得
        uniform_image = Image.open(self.get_resolve_path(f"{config.PLAYER_UNIFORM_FOLDER_PATH}/uniform_{number}.png")).resize((config.PLAYER_IMAGE_WIDTH,config.PLAYER_IMAGE_HEIGHT))
        #背景のピッチ画像を取得
        formation_image = Image.open(self.get_resolve_path(config.FORMATION_IMAGE_PATH)).convert("RGBA")

        #ユニ画像の透過を効かせるため、スタメン画像と同じサイズの透明な画像を用意して載せる https://qiita.com/iso12800jp/items/a74852ebfd3041065aeb
        clear_back_img_for_uniform = Image.new("RGBA", formation_image.size, (255, 255, 255, 0))
        clear_back_img_for_uniform.paste(uniform_image, player_image_position)

        #ユニ画像合成
        formation_image = Image.alpha_composite(formation_image, clear_back_img_for_uniform)

        #選手名の背景描画
        #透過したいので、透過用の背景を作る https://teratail.com/questions/132373
        clear_back_img_for_name_back = Image.new("RGBA", formation_image.size, (255, 255, 255, 0))
        #透過背景に対してdraw
        draw = ImageDraw.Draw(clear_back_img_for_name_back)
        font = ImageFont.truetype(self.get_resolve_path(config.FONT_PATH), config.PLAYER_NAME_FONT_SIZE)

        #背景をつける範囲を取得（名前の座標は中央なので背景エリアの左上、右下の座標をマージン込みで算出）
        #TODO:名前が一定以上長くなった場合2列にしたほうがいい
        #選手名を入れる座標取得（X座標はユニ画像サイズの半分右に、Y座標は30上にそれぞれユニ画像の座標からずらす）
        player_name_position = (player_image_position[0]+config.HALF_PLAYER_IMAGE_SIZE, player_image_position[1]-config.OFFSET_PLAYERNAME_Y_POSITION)

        player_name_area = draw.textsize(player_name, font)
        name_x = player_name_position[0]
        name_y = player_name_position[1]
        #背景のマージン8くらいとっとく
        name_x_offset = player_name_area[0]/2+8
        name_y_offset = player_name_area[1]/2+8
        player_name_backgroud_position = (name_x-name_x_offset, name_y-name_y_offset, name_x+name_x_offset, name_y+name_y_offset)

        #背景は半透明な白
        draw.rectangle(player_name_backgroud_position, fill=(255,255,255,180))
        #選手名背景合成
        formation_image = Image.alpha_composite(formation_image, clear_back_img_for_name_back)

        #選手名描画。こちらは元の画像に描画する（既に背景が入ってる状態）
        draw = ImageDraw.Draw(formation_image)
        #文字描画
        draw.text(player_name_position, player_name, font=font, fill="black", align="center", anchor="mm")
        #編集し終わったピッチ画像を保存
        formation_image.save(self.get_resolve_path(config.FORMATION_IMAGE_PATH))

        #TODO:画像をs3に保存してそのパスを返す

    def get_resolve_path(self, path:str):
        """
        絶対パスを取得する

        :param path: このファイルからの相対パス
        :type path: str
        :return: 絶対パス
        :rtype: str
        """
        current_path = os.getcwd()
        return f"{current_path}/jleague-api/controller/{path}"