import scrapy
import openpyxl
from scrapy import Selector, Request
from scrapy.http import HtmlResponse
from ..items import BiliRoomInfoItem


class RoomInfoSpider(scrapy.Spider):
    name = "roominfo"
    allowed_domains = ["live.bilibili.com"]
    start_urls = ["https://live.bilibili.com/p/eden/"]
    

    def start_requests(self):
        with open('../RoomsId_during.txt', 'r') as f:
            rooms_li = f.readlines()

        base_url = 'https://api.live.bilibili.com/xlive/lottery-interface/v1/lottery/getLotteryInfoWeb?'
        for room in rooms_li:
            room.strip()
            # print()
            room_id, room_block = room.split(' ')[0],room.split(' ')[1]
            sub_url = base_url+f'roomid={room_id}'
            yield Request(url=sub_url,callback=self.parse,cb_kwargs={'block': room_block,'roomid':room_id})  # 设置代理        

    def parse(self, response: HtmlResponse, **kwargs):
        block = kwargs['block']
        roomid = kwargs['roomid']
        sel = Selector(response).extract()
        data = sel.get('data', '')
        roominfo_item = BiliRoomInfoItem()
        roominfo_item['pocket_info'] = data
        roominfo_item['room_block'] = block
        roominfo_item['room_id'] = roomid
        yield roominfo_item

