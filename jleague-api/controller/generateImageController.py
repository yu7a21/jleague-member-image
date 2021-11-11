#https://hashikake.com/Pillow
from PIL import Image, ImageDraw, ImageFont, ImageChops
import os, shutil
from model.player import Player
from model.team import Team

#画像フォルダ
RESOURCE_FOLDER_PATH = "../resource"
#背番号を入れたユニ画像を入れるフォルダ
PLAYER_UNIFORM_FOLDER_PATH = f"{RESOURCE_FOLDER_PATH}/player_uniform"
#ピッチの初期画像
INIT_FIELD_IMAGE_PATH = f"{RESOURCE_FOLDER_PATH}/soccer_field.jpeg"
#ユニの初期画像
INIT_UNIFORM_IMAGE_PATH = f"{RESOURCE_FOLDER_PATH}/uniform_white.png"
#フォントファイル
FONT_PATH = f"{RESOURCE_FOLDER_PATH}/font/smartphoneui.otf"
#チームカラーに色置換したユニ画像
TEAM_COLOR_UNIFORM_PATH = f"{RESOURCE_FOLDER_PATH}/team_color_uniform.png"
#完成画像
FORMATION_IMAGE_PATH = f"{RESOURCE_FOLDER_PATH}/formation_image.jpeg"


PLAYER_IMAGE_WIDTH=80 #スタメン画像に表示するときのユニ画像の1辺
PLAYER_IMAGE_HEIGHT=81 #スタメン画像に表示するときのユニ画像の1辺
HALF_PLAYER_IMAGE_SIZE = int(PLAYER_IMAGE_WIDTH/2) #ユニ画像の1辺の半分。選手名描画の座標で使うが普通に2でわるとfloatになるのでここでintにしてる
OFFSET_PLAYERNAME_Y_POSITION = 30 #ユニ画像からどれだけ上に選手名を描画するか
PLAYER_NAME_FONT_SIZE = 30 #選手名のフォントサイズ
UNIFORM_NUMBER_FONT_SIZE = 250 #背番号のフォントサイズ

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

#各フォーメーションごと、ポジションの座標データ
#座標取得:http://wisteriahill.sakura.ne.jp/OpenCV/getArea4Haartraining/
mock_position_position_data = {
    "4-4-2":{
        "RCF": (330,260),
        "LCF": (330,462),
        "RW": (566,96),
        "RCM": (566,260),
        "LCM": (566,462),
        "LW": (566,632),
        "RSB": (801,96),
        "RCB": (801,260),
        "LCB": (801,462),
        "LSB": (801,632),
        "GK": (1027,378),
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

#TODO:パスは定数化する
def generate_image(image_info:dict = mock_image_info, position_data:dict = mock_position_data):
    #先に画像色をチームカラーに置換
    color_list = Team.query.filter_by(id=image_info["team_id"]).first().color.split(",")
    team_color = (int(color_list[0]), int(color_list[1]), int(color_list[2]))
    put_uniform_color(team_color)

    #背番号を全選手分いれる
    if not os.path.exists(get_resolve_path(PLAYER_UNIFORM_FOLDER_PATH)):
        os.mkdir(get_resolve_path(PLAYER_UNIFORM_FOLDER_PATH))
    for position, number in position_data.items():
        generate_uniform_image(str(number))

    #先にピッチ画像をコピーしておく
    Image.open(get_resolve_path(INIT_FIELD_IMAGE_PATH)).copy().save(get_resolve_path(FORMATION_IMAGE_PATH))

    #背番号とポジションの対応を見て各ポジションにユニ画像・名前文字列を配置
    for position, number in position_data.items():
        generate_formation_image(image_info["formation"], image_info["team_id"], position, number)

    #全選手分作ったユニを削除
    shutil.rmtree(get_resolve_path(PLAYER_UNIFORM_FOLDER_PATH))

    #色変更した画像削除
    os.remove(get_resolve_path(TEAM_COLOR_UNIFORM_PATH))

    #TODO:完成したスタメン画像返す https://takake-blog.com/python-flask/#2
    return "success"

def generate_formation_image(formation, team_id, position_name, number):
    """
    スタメン画像に1選手のユニ画像・名前を入れる

    :param formation: [description]
    :type formation: [type]
    :param team_id: [description]
    :type team_id: [type]
    :param position_name: [description]
    :type position_name: [type]
    :param number: [description]
    :type number: [type]
    """
    #TODO:英語名と日本語名選べるようにする？
    player_name = Player.query.filter_by(team_id=team_id, number=number).first().name_ja

    #各ポジションのピッチ画像上の座標（左上がこの座標にあう）https://note.nkmk.me/python-pillow-paste/
    player_image_position = mock_position_position_data[formation][position_name]
    #選手名を入れる座標は、X座標はユニ画像サイズの半分右に、Y座標は30上にそれぞれユニ画像の座標からずらす
    player_name_position = (player_image_position[0]+HALF_PLAYER_IMAGE_SIZE, player_image_position[1]-OFFSET_PLAYERNAME_Y_POSITION)

    #ユニ画像を小さくリサイズして取得
    uniform_image = Image.open(get_resolve_path(f"{PLAYER_UNIFORM_FOLDER_PATH}/uniform_{number}.png")).resize((PLAYER_IMAGE_WIDTH,PLAYER_IMAGE_HEIGHT))
    #背景のピッチ画像を取得
    formation_image = Image.open(get_resolve_path(FORMATION_IMAGE_PATH))

    formation_image.paste(uniform_image, player_image_position)

    #選手名を描画
    draw = ImageDraw.Draw(formation_image)
    font = ImageFont.truetype(get_resolve_path(FONT_PATH), PLAYER_NAME_FONT_SIZE)
    #TODO:選手名の背景は色つけた方が見やすいかも https://code-de-byouga.hatenablog.com/entry/pillow-text
    draw.text(player_name_position, player_name, font=font, fill="black", align="center", anchor="mm")

    #編集し終わったピッチ画像を保存
    formation_image.save(get_resolve_path(FORMATION_IMAGE_PATH))

def generate_uniform_image(number:str):
    """
    ユニフォームに背番号を入れる

    """
    uniform_img = Image.open(get_resolve_path(TEAM_COLOR_UNIFORM_PATH))
    #描画開始
    draw = ImageDraw.Draw(uniform_img)
    #フォント読み込み
    font = ImageFont.truetype(get_resolve_path(FONT_PATH), UNIFORM_NUMBER_FONT_SIZE)
    #文字描画(anchorは指定座標が文字エリアのどこにくるかの設定。この場合中央)
    draw.text((407, 331), number, font=font, fill="black", align="center", anchor="mm")
    #画像保存
    uniform_img.save(get_resolve_path(f"{PLAYER_UNIFORM_FOLDER_PATH}/uniform_{number}.png"))


#処理内容:https://qiita.com/pashango2/items/d6dda5f07109ee5b6163
def put_uniform_color(team_color:tuple):
    """
    元のユニフォーム画像をチームカラーに変換

    :param team_color: [description]
    :type team_color: tuple
    """
    uniform_img = Image.open(get_resolve_path(INIT_UNIFORM_IMAGE_PATH))
    default_color = (255,255,255)
    r, g, b, a = uniform_img.split()

    _r = r.point(lambda _: 1 if _ == default_color[0] else 0, mode="1")
    _g = g.point(lambda _: 1 if _ == default_color[1] else 0, mode="1")
    _b = b.point(lambda _: 1 if _ == default_color[2] else 0, mode="1")
    _a = a.point(lambda _: 1 if _ == 0 else 0, mode="1")

    mask = ImageChops.logical_and(_r, _g)
    mask = ImageChops.logical_and(mask, _b)

    uniform_img.paste(Image.new("RGB", uniform_img.size, team_color), mask=mask)
    uniform_img.save(get_resolve_path(TEAM_COLOR_UNIFORM_PATH))

def get_resolve_path(path:str):
    current_path = os.getcwd()
    return f"{current_path}/jleague-api/controller/{path}"

if __name__ == "__main__":
    generate_image()