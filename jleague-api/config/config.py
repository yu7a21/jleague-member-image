import os

DB_HOST = os.getenv("DB_HOST")
DB_DATABASE = os.getenv("DB_DATABASE")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

#画像フォルダ
RESOURCE_FOLDER_PATH = "../resource"
#背番号を入れたユニ画像を入れるフォルダ
PLAYER_UNIFORM_FOLDER_PATH = f"{RESOURCE_FOLDER_PATH}/player_uniform"
#ピッチの初期画像
INIT_FIELD_IMAGE_PATH = f"{RESOURCE_FOLDER_PATH}/soccer_field.jpeg"
#ユニの初期画像
DEFAULT_UNIFORM_IMAGE_PATH = f"{RESOURCE_FOLDER_PATH}/default_uniform.png"
#フォントファイル
FONT_PATH = f"{RESOURCE_FOLDER_PATH}/font/corporatelogo.ttf"
#チームカラーに色置換したユニ画像
TEAM_COLOR_UNIFORM_PATH = f"{RESOURCE_FOLDER_PATH}/team_color_uniform.png"
#完成画像
FORMATION_IMAGE_PATH = f"{RESOURCE_FOLDER_PATH}/formation_image.png"

#スタメン画像に表示するときのユニ画像の1辺
PLAYER_IMAGE_WIDTH=90
#スタメン画像に表示するときのユニ画像の1辺
PLAYER_IMAGE_HEIGHT=81
#ユニ画像の1辺の半分。選手名描画の座標で使うが普通に2でわるとfloatになるのでここでintにしてる
HALF_PLAYER_IMAGE_SIZE = int(PLAYER_IMAGE_WIDTH/2)
#ユニ画像からどれだけ上に選手名を描画するか
OFFSET_PLAYERNAME_Y_POSITION = 30
#選手名のフォントサイズ
PLAYER_NAME_FONT_SIZE = 30
#ユニ画像に入れる背番号の座標
UNIFORM_NUMBER_POSITION = (407, 331)
#背番号のフォントサイズ
UNIFORM_NUMBER_FONT_SIZE = 250