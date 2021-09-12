from db import Db
from config import mst_data

def init_migrate():
    table_name = "team"
    team_data = mst_data.team

    db = Db()
    db.create_table(table_name)

    db.insert(table_name, team_data)

if __name__ == "__main__":
    init_migrate()