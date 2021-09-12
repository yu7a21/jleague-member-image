from config import config
from config import table_config

import pymysql
import pymysql.cursors as cursors

class Db():
    def __init__ (self):
        self.table_config = table_config.table_struct_list
    
    def exec_post_query(self, query):
        """
        POST系のクエリを実行する(INSERTなど)。

        Parameters
        -----------
        query : str
            実行するクエリ文。
        """
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
        """
        GET系のクエリを実行する(SELECTなど)。

        Parameters
        -----------
        query : str
            実行するクエリ文。

        Returns
        -----------
        result : dict
            取得したデータ。
        """
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
        """
        テーブルを作成する。

        Parameters
        ----------
        table_name : str
            テーブル名。

        """
        columns = self.table_config[table_name]

        column_query_list = []
        for column in columns:
            column_query_list.append(self.make_create_column_query(column, columns[column]))
                
        init_query = f"CREATE TABLE {table_name}"
        column_query = ",".join(column_query_list)

        query = f"{init_query}({column_query})"

        self.exec_post_query(query)
    
    def insert(self, table_name, row_datas):
        """
        DBに値を挿入する

        Parameters
        ----------
        table_name : str
            挿入先のテーブル名。
        row_datas : list
            挿入するデータ。各要素はカラム名をキーにしたdict。

        """
        table_config = self.table_config[table_name]

        insert_query_list = []
        query_list = []
        column_list = []

        #VALUES以降の文を作る
        for row in row_datas:
            for key in row:
                #VARCHARのカラムに挿入するデータはダブルクォーテーションで囲む
                if "VARCHAR" in table_config[key]["type"]:
                    insert_query_list.append(f"\"{row[key]}\"") 
                else:
                    insert_query_list.append(f"{row[key]}") 
            data_str = ",".join(insert_query_list)
            query_list.append(f"({data_str})")
            insert_query_list.clear()
        
        #INSERTするカラムを指定するための文を作る
        for key in row_datas[0]:
            # auto_incrementのカラムだった場合はスルー
            if table_config[key]["auto_increment"]:
                continue
            column_list.append(key)
            
        
        init_query = f"INSERT INTO {table_name}"
        insert_query = ",".join(query_list)
        column_str = ",".join(column_list)
        column_query = f"({column_str})"

        query = f"{init_query} {column_query} VALUES {insert_query}"

        self.exec_post_query(query)
    
    def get_all_items(self, table_name):
        """
        テーブルの内容をすべて取得する

        Parameters
        -----------
        table_name : str
            取得するテーブル名。

        """
        query = f"SELECT * FROM {table_name}"
        return self.exec_get_query(query)
    
    def make_create_column_query(self, name, column):
        """
        INSERT文で使う各カラムの設定部分を作成する

        Parameters
        ----------
        name : str
            カラム名。
        column : dict
            カラムの設定値。

        """
        type = column["type"]
        not_null = "NOT NULL" if column["not_null"] else ""
        prymary_key = "PRIMARY KEY" if column["primary_key"] else ""
        auto_increment = "AUTO_INCREMENT" if column["auto_increment"] else ""

        return f"{name} {type} {not_null} {prymary_key} {auto_increment}"

