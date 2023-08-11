import scrapy
from scrapy import Selector, Request
from scrapy.http import HtmlResponse
from ..items import BiliRoomInfoItem


class RoomInfoSpider(scrapy.Spider):
    name = "roominfo_b1"
    allowed_domains = ["live.bilibili.com"]
    start_urls = ["https://live.bilibili.com/p/eden/"]
    

    def start_requests(self):
        with open('../RoomsId_during.txt', 'r') as f:
            rooms_li = f.readlines()
        # b1rooms_li = []
        # for room in rooms_li:
            # if 'xuni' in room or 'diantai' in room:
            #     b1rooms_li.append(room)
        # print('该分区个数:',len(b1rooms_li),b1rooms_li)
        base_pocket_url = 'https://api.live.bilibili.com/xlive/lottery-interface/v1/lottery/getLotteryInfoWeb?'
        for room in rooms_li:
            room.strip()
            room_id, u_id, room_block = room.split(' ')[0],room.split(' ')[1],room.split(' ')[2]
            sub_pocket_url = base_pocket_url+f'roomid={room_id}' 
            yield Request(url=sub_pocket_url,callback=self.pocket_parse,cb_kwargs={'block': room_block,'roomid':room_id, 'uid': u_id})  # 设置代理        

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
            sub_uid_url = base_person_num_url+f'ruid={u_id}&roomId={roomid}&page=1&pageSize=50'
            yield  Request(url=sub_uid_url,callback=self.personnum_parse,cb_kwargs={'roominfo_item': roominfo_item})  # 设置代理   
    
    def personnum_parse(self, response: HtmlResponse, **kwargs):
        roominfo_item = kwargs['roominfo_item']
        sel = Selector(response).extract()
        personnum_data = sel.get('data', '')
        roominfo_item['person_num'] = personnum_data
        yield roominfo_item



