import copy
import os
import sqlite3

import scrapy
from fake_useragent import UserAgent
from scrapy import Selector, Request
from scrapy.http import HtmlResponse

from ..items import BiliRoomInfoItem


class RoomInfoSpider(scrapy.Spider):
    name = "roominfo_b1"
    allowed_domains = ["live.bilibili.com"]
    start_urls = ["https://live.bilibili.com/p/eden/"]

    def start_requests(self):
        basedir = os.path.abspath(os.path.dirname(__file__)).replace(
            "\\app\\bili_pocket\\bili_roominfo_block1\\bili_roominfo\\spiders",
            "")
        conn = sqlite3.connect(os.path.join(basedir, "app.db"))
        cursor = conn.cursor()
        query = "SELECT * FROM room"
        cursor.execute(query)
        results = cursor.fetchall()
        rooms = copy.deepcopy(results)
        query = "SELECT * FROM pocket"
        cursor.execute(query)
        pocket = cursor.fetchall()
        # 创建一个新的列表用于存储过滤后的rooms
        filtered_rooms = []

        # 遍历rooms
        for room in rooms:
            room_id = room[2]  # 获取room_id

            # 检查rooms中的room_id是否存在于pocket中
            exists_in_pocket = any(room_id == pocket_row[0] for pocket_row in pocket)

            # 如果room_id不存在于pocket中，则将该元素添加到filtered_rooms中
            if not exists_in_pocket:
                filtered_rooms.append(room)

        # # 打印过滤后的rooms
        # for room in filtered_rooms:
        #     print(room)
        base_pocket_url = 'https://api.live.bilibili.com/xlive/lottery-interface/v1/lottery/getLotteryInfoWeb?'
        for room in filtered_rooms:
            # room.strip()
            room_id, u_id, room_block = room[2], room[1], room[4]
            sub_pocket_url = base_pocket_url + f'roomid={room_id}'
            user_agent = UserAgent()
            headers = {'User-Agent': user_agent.random}
            yield Request(url=sub_pocket_url, headers=headers, callback=self.pocket_parse,
                          cb_kwargs={'block': room_block, 'roomid': room_id, 'uid': u_id})  # 设置代理

    def pocket_parse(self, response: HtmlResponse, **kwargs):
        u_id = kwargs['uid']
        block = kwargs['block']
        roomid = kwargs['roomid']
        sel = Selector(response).extract()
        # print('----------------------------------',sel)
        data = sel.get('data', '')
        if not data.get('popularity_red_pocket') and not data.get('anchor'):
            return
        else:
            roominfo_item = BiliRoomInfoItem()
            roominfo_item['pocket_info'] = data
            roominfo_item['room_block'] = block
            roominfo_item['room_id'] = roomid

            base_person_num_url = 'https://api.live.bilibili.com/xlive/general-interface/v1/rank/getOnlineGoldRank?'
            sub_uid_url = base_person_num_url + f'ruid={u_id}&roomId={roomid}&page=1&pageSize=50'
            yield Request(url=sub_uid_url, callback=self.personnum_parse,
                          cb_kwargs={'roominfo_item': roominfo_item})  # 设置代理

    def personnum_parse(self, response: HtmlResponse, **kwargs):
        roominfo_item = kwargs['roominfo_item']
        sel = Selector(response).extract()
        personnum_data = sel.get('data', '')
        roominfo_item['person_num'] = personnum_data
        yield roominfo_item
