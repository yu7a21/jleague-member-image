import requests
import json
from bs4 import BeautifulSoup
from logging import getLogger ,config

from db import Db


def get_players():
    """
    JLeague Data Siteから全選手データを取得する

    """
    with open("./config/log_config.json", "r") as f:
        log_conf = json.load(f)
    config.dictConfig(log_conf)
    logger = getLogger(__name__)

    db = Db()
    team_list = db.get_all_items("team")

    players_page_url = "https://data.j-league.or.jp/SFIX02/search?displayId=SFIX02&selectValue={}&displayId=SFIX02&selectValueTeam={}&displayName={}&displayNameTeam={}"
    player_list = []

    for team in team_list:
        league = team["league"]
        select_value = "1" if league == "J1" else "2" if league == "J2" else "3"
        team_id = team["id"]
        select_value_team = str(team_id)
        display_name = league + "リーグ"
        display_name_team = team["name"]

        logger.info(f"\"{display_name_team}\"のデータ取得開始")

        
        url = players_page_url.format(select_value, select_value_team, display_name, display_name_team)
        response = requests.get(url)
                
        soup = BeautifulSoup(response.text, 'html.parser')
        name_list = soup.select('.name')
        for name in name_list:
            player_info = []
            #取得した名前列から不要な文字を排除
            name_str = str(name.text.split(",")).replace("['", "").replace("[\"", "").replace("']", "").replace("\"]", "").replace("\\r\\n\\t\\t\\t\\t\\t\\t\\t\\t\\t\\t\\t\\t", "").replace("\\xa0",",").replace("\\u3000", " ").replace("\\n",",").replace("（２種）", "").replace("ホームグロウン","").split(',')
            #replaceによって挟まれた空文字を排除
            for string in filter(lambda s: s != "", name_str):
                player_info.append(string)
            #背番号が空の場合がある
            if len(player_info) == 3:
                name_ja = player_info[1]
                name_en = player_info[2]
                number = player_info[0]
            else:
                name_ja = player_info[0]
                name_en = player_info[1]
                number = "999"
            player_list.append({"team_id":team_id, "name_ja":name_ja, "name_en":name_en, "number":number})
        logger.info(f"\"{display_name_team}\"のデータ取得終了")
    
    logger.info("DBへの保存開始")
    db.insert("player", player_list)
    logger.info("DBへの保存終了")

if __name__ == "__main__":
    get_players()