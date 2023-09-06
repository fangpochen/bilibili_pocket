import random
import sqlite3
import time
from concurrent.futures import ThreadPoolExecutor

import requests


class B_packet:
    def __init__(self):
        self.count = 0

        # 隧道域名:端口号
        tunnel = "w315.kdltps.com:15818"

        # 用户名密码方式
        username = "t19324046673050"
        password = "dyy1xeiq"
        # 白名单方式（需提前设置白名单）
        self.proxies = {
            "http": "http://%(user)s:%(pwd)s@%(proxy)s/" % {"user": username, "pwd": password, "proxy": tunnel},
            "https": "http://%(user)s:%(pwd)s@%(proxy)s/" % {"user": username, "pwd": password, "proxy": tunnel}
        }

        # self.proxies = None
        self.db_name = "F:\下载\\bilibili_pocket\\app.db"

        self.table_name = "pocket"
        self.connection = sqlite3.connect(self.db_name, check_same_thread=False)
        self.cursor = self.connection.cursor()

        # 检查指定表是否存在
        # self.cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{self.table_name}'")
        # table_exists = self.cursor.fetchone()

        # # 如果不存在则创建表
        # if not table_exists:
        #     self.cursor.execute(f'''CREATE TABLE IF NOT EXISTS {self.table_name}
        #                                                   (id INTEGER PRIMARY KEY AUTOINCREMENT,
        #                                                   uid TEXT,
        #                                                   roomid TEXT,
        #                                                   主播名称 TEXT,
        #                                                   房间标题 TEXT,
        #                                                   在线人数 TEXT,
        #                                                   红包价值 TEXT,
        #                                                   剩余时间 TEXT,
        #                                                   监测时间 TEXT)''')

    def check_duplicate_data(self, data):
        """
            根据指定字段判断表中是否已有指定数据
        """
        query = f"SELECT COUNT(*) FROM {self.table_name} WHERE roomid=?"
        self.cursor.execute(query, (data["roomid"],))
        count = self.cursor.fetchone()[0]
        return count > 0

    def insert_info(self, data):
        """
            插入数据
            传入字典列表里的数据到数据库
        """
        while True:
            try:
                # if not self.check_duplicate_data(data):
                self.cursor.execute(
                    f"INSERT INTO {self.table_name} (uid, room_id, room_name,room_title,total_p,price,leave_time,update_time) "
                    f"VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                    (data["uid"], data["roomid"], data["主播名称"], data["房间标题"], data["在线人数"], data["红包价值"],
                     data["剩余时间"], data["监测时间"]))
                break
            except Exception as err:
                print(err)
                time.sleep(0.5)
                continue

    def clear_table(self):
        """
            删除表的所有数据再新建表
        """
        # 检查指定表是否存在
        self.cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{self.table_name}'")
        table_exists = self.cursor.fetchone()

        # 如果存在删除这个库的这个表
        if table_exists:
            # 删除表
            self.cursor.execute(f"DROP TABLE {self.table_name}")

            self.cursor.execute(f'''CREATE TABLE IF NOT EXISTS {self.table_name}
                                                                      (id INTEGER PRIMARY KEY AUTOINCREMENT,
                                                                      uid TEXT,
                                                                      roomid TEXT,
                                                                      主播名称 TEXT,
                                                                      房间标题 TEXT,
                                                                      在线人数 TEXT,
                                                                      红包价值 TEXT,
                                                                      剩余时间 TEXT,
                                                                      监测时间 TEXT)''')
            self.connection.commit()

    def convert_time_(self, timestamp):
        timeArray = time.localtime(timestamp)
        otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
        return otherStyleTime

    def get_onlineNum(self, uid):
        while True:
            try:
                onlineNum = requests.get(
                    f'https://api.live.bilibili.com/xlive/general-interface/v1/rank/getOnlineGoldRank?ruid={uid}&roomId=111111&page=1&pageSize=50',
                    proxies=self.proxies).json()['data']['onlineNum']
                break
            except:
                time.sleep(0.5)
                continue
        return onlineNum

    def get_packet(self, roomid):
        headers = {
            'referer': f'https://live.bilibili.com/{random.randrange(1, 9)}{random.randrange(1, 9)}{random.randrange(1, 9)}{random.randrange(1, 9)}{random.randrange(1, 9)}{random.randrange(1, 9)}{random.randrange(1, 9)}{random.randrange(1, 9)}',
            "user-agent": f"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{random.randrange(1, 9)}{random.randrange(1, 9)}{random.randrange(1, 9)}.{random.randrange(1, 9)}.{random.randrange(1, 9)}.{random.randrange(1, 9)} Safari/537.36"
        }
        while True:
            try:
                response = requests.get(
                    f'https://api.live.bilibili.com/xlive/lottery-interface/v1/lottery/getLotteryInfoWeb?roomid={roomid}',
                    headers=headers, proxies=self.proxies).json()['data']['popularity_red_pocket'][0]
                break
            except:
                time.sleep(0.5)
                continue
        total_price = response["total_price"]
        remaining_time = response["end_time"] - response["current_time"]
        return total_price, remaining_time

    def search(self, page):
        response = requests.get(
            f'https://api.live.bilibili.com/xlive/web-interface/v1/second/getUserRecommend?page={page}&page_size=30&platform=web',
            proxies=self.proxies)
        for i in response.json()['data']['list']:
            data = {}
            data['uid'] = i['uid']
            data['roomid'] = i['roomid']
            data['主播名称'] = i['uname']
            data['房间标题'] = i['title']
            red_packet = '否'
            for key, value in i['pendant_info'].items():
                if value['content'] == '红包':
                    red_packet = '是'

            if red_packet == '是':
                data['在线人数'] = self.get_onlineNum(i['uid'])
                data['红包价值'], data['剩余时间'] = self.get_packet(i['roomid'])
                data['监测时间'] = self.convert_time_(time.time())
                self.insert_info(data)
                self.count += 1
                print(page, self.count, data)

    def main(self):
        while True:
            # self.clear_table()
            pool = ThreadPoolExecutor(max_workers=15)
            tasks = [pool.submit(self.search, page) for page in range(1, 950)]
            for t in tasks:
                t.result()
            self.connection.commit()
            print("监控完毕")
            time.sleep(60)


B_packet().main()
