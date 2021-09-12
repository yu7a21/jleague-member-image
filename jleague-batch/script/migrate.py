from db import Db
from config import mst_data

def init_migrate():
    table_names = ["team","player"]
    team_data = mst_data.team

    db = Db()
    for table_name in table_names:
        db.create_table(table_name)

    db.insert("team", team_data)

if __name__ == "__main__":
    init_migrate()