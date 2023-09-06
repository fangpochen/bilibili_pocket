import sqlite3
import pandas as pd


class Sqlit:
    def __init__(self):
        self.db_name = '数据库.db'
        self.table_name = 'B站'
        self.connection = sqlite3.connect(self.db_name)
        self.cursor = self.connection.cursor()

    def get_table_info(self):
        """
            查询该表的所有数据并打印输出
        """

        self.cursor.execute(f"SELECT * FROM {self.table_name}")
        rows = self.cursor.fetchall()

        self.cursor.execute(f"PRAGMA table_info({self.table_name})")
        columns = [column[1] for column in self.cursor.fetchall()]
        n = 0
        for row in rows:
            row_dict = dict(zip(columns, row))
            n += 1
            print(n, row_dict)

    def info_to_xlsx(self):
        """
            将该表的所有数据导出为xlsx
        """
        # 读取数据到 pandas 数据框
        df = pd.read_sql_query(f"SELECT * FROM {self.table_name}", self.connection)
        df.to_excel(f"./{self.table_name}.xlsx", index=False)

Sqlit().get_table_info()
Sqlit().info_to_xlsx()
