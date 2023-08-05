import scrapy
from scrapy import Selector, Request
from scrapy.http import HtmlResponse
from ..items import BiliRoomIdItem


class RoomIdSpider(scrapy.Spider):
    name = "roomid"
    allowed_domains = ["live.bilibili.com"]
    start_urls = ["https://live.bilibili.com/p/eden/"]
    

    def start_requests(self):
        base_url = 'https://api.live.bilibili.com/xlive/web-interface/v1/second/getList?platform=web&parent_area_id='
        block = {'xuni':f'{base_url}9&area_id=0&sort_type=sort_type_291&page',
                'diantai':f'{base_url}5&area_id=0&sort_type=sort_type_225&page',
                'yuele':f'{base_url}1&area_id=0&sort_type=sort_type_152&page',
                'gouwu':f'{base_url}300&area_id=0&sort_type=online&page',
                'danji':f'{base_url}6&area_id=0&sort_type=sort_type_150&page',
                'saishi':f'{base_url}13&area_id=0&sort_type=online&page',
                'zhishi':f'{base_url}11&area_id=0&sort_type=sort_type_308&page',
                'shenghuo':f'{base_url}10&area_id=0&sort_type=sort_type_269&page',
                'wangyou':f'{base_url}2&area_id=0&sort_type=sort_type_124&page',
                'shouyou':f'{base_url}3&area_id=0&sort_type=sort_type_121&page'}
        # block = {'gouwu':f'{base_url}300&area_id=0&sort_type=online&page',
        #      'danji':f'{base_url}6&area_id=0&sort_type=sort_type_150&page'}        
        for key,val in block.items():
            url = val
            if key in ['xuni','yuele', 'diantai']:
                for page in range(1,80):
                    page_str = f'={page}'
                    sub_url = url+page_str
                    yield Request(url=sub_url,callback=self.parse, cb_kwargs={'block': key})  # 设置代理
            else:
                for page in range(1,20):
                    page_str = f'={page}'
                    sub_url = url+page_str
                    yield Request(url=sub_url,callback=self.parse, cb_kwargs={'block': key})  # 设置代理


    def parse(self, response: HtmlResponse, **kwargs):
        block = kwargs['block']
        sel = Selector(response).extract()
        data = sel.get('data', '')
        rooms_li = data.get('list','')
        print('------------------------------',len(rooms_li))
        if rooms_li:
            for roominfo in rooms_li:
                print(roominfo['roomid'])
                room_item = BiliRoomIdItem()
                room_item['roomid'] = roominfo.get('roomid','')
                room_item['roomblock'] = block
                yield room_item
        else:
            return
    
