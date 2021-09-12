from config import config
from config import table_config

import pymysql
import pymysql.cursors as cursors

class Db():
    def __init__ (self):
        self.table_config = table_config.table_struct_list
    
    def exec_post_query(self, query):
        connect = pymysql.connect(
            user=config.db_user,
            passwd=config.db_password,
            host=config.db_host,
            db=config.db_database,
            charset="utf8",
            cursorclass=cursors.DictCursor
        )

        with connect:
            with connect.cursor() as cursor:
                cursor.execute(query)
            connect.commit()
    
    def exec_get_query(self, query):
        connect = pymysql.connect(
            user=config.db_user,
            passwd=config.db_password,
            host=config.db_host,
            db=config.db_database,
            charset="utf8",
            cursorclass=cursors.DictCursor
        )

        with connect:
            with connect.cursor() as cursor:
                cursor.execute(query)
                result = cursor.fetchall()
        return result

    def create_table(self, table_name):
        columns = self.table_config[table_name]

        column_query_list = []
        for column in columns:
            column_query_list.append(self.make_create_column_query(column, columns[column]))
                
        init_query = f"CREATE TABLE {table_name}"
        column_query = ",".join(column_query_list)

        query = f"{init_query}({column_query})"

        self.exec_post_query(query)
    
    def insert(self, table_name, row_data):
        table_config = self.table_config[table_name]

        insert_query_list = []
        query_list = []
        for row in row_data:
            for key in row:
                if "VARCHAR" in table_config[key]["type"]:
                    insert_query_list.append(f"\"{row[key]}\"") 
                else:
                    insert_query_list.append(f"{row[key]}") 
            data_str = ",".join(insert_query_list)
            query_list.append(f"({data_str})")
            insert_query_list.clear()
        
        init_query = f"INSERT INTO {table_name} VALUES"
        insert_query = ",".join(query_list)

        query = f"{init_query} {insert_query}"
        self.exec_post_query(query)
    
    def get_all_items(self, table_name):
        query = f"SELECT * FROM {table_name}"
        return self.exec_get_query(query)
    
    def make_create_column_query(self, name, column):
        type = column["type"]
        not_null = "NOT NULL" if column["not_null"] else ""
        prymary_key = "PRIMARY KEY" if column["primary_key"] else ""
        auto_increment = "AUTO_INCREMENT" if column["auto_increment"] else ""

        return f"{name} {type} {not_null} {prymary_key} {auto_increment}"

