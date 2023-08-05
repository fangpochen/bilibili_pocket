# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


import datetime
# useful for handling different item types with a single interface
import time

from app.models import Pocket, Tian
from app.mysql_util import save_list


class BiliRoomInfoPipeline:
    def __init__(self) -> None:
        self.blocknumdict = {}
        self.pocket_li = []
        self.tianxuan_li = []
        self.base_url = 'https://live.bilibili.com/'

    def close_spider(self, spider):
        # print(self.blocknumdict)
        self.pocket_li.sort(key=lambda ele: ele[3], reverse=True)  # indx3是红包价值
        self.tianxuan_li.sort(key=lambda ele: ele[2])  # indx2是天选价值
        pocket_arr = []
        for pocket in self.pocket_li:
            update_time = datetime.datetime.now()
            pocket_data = Pocket(price=pocket[3],
                                 room_id=pocket[5].replace('https://live.bilibili.com/', ''),
                                 leave_time=pocket[0],
                                 update_time=update_time,
                                 )
            pocket_arr.append(pocket_data)
            print('最终红包信息-----------------', pocket)
        save_list(pocket_arr)

        tian_arr = []
        for tian in self.tianxuan_li:
            update_time = datetime.datetime.now()
            tian_data = Tian(price=tian[2],
                             room_id=tian[5].replace('https://live.bilibili.com/', ''),
                             leave_time=tian[0],
                             update_time=update_time,
                             )
            tian_arr.append(tian_data)
            print('最终天选信息-----------------', tian)
        save_list(pocket_arr)

    def process_item(self, item, spider):
        self.pocket_info = item.get('pocket_info', '')
        self.block = item.get('room_block', '')
        self.roomid = item.get('room_id', '')
        self.cur_url = self.base_url + str(self.roomid)
        if self.pocket_info.get('popularity_red_pocket'):
            popul_pocket = self.get_popular_pocket()
            if popul_pocket:
                self.pocket_li.append(popul_pocket)
            # if len(self.pocket_li) %5 == 0:  # 红包满足10的倍数排一次序
            #     self.pocket_li.sort(key=lambda ele:ele[3],reverse=True)  # indx3是红包价值
            #     for pocket in self.pocket_li:
            #         print('红包信息-----------------',pocket)

        if self.pocket_info.get('anchor'):
            tianxuan = self.get_tianxuan()
            if tianxuan:
                self.tianxuan_li.append(tianxuan)
            # if len(self.tianxuan_li) %5 == 0:  # 天选满足5的倍数排一次序
            #     for tian in self.tianxuan_li:
            #         print('天选信息-----------------',tian)

    def get_popular_pocket(self):
        timestamp = time.time()  # 获取当前时间戳
        pop_pocket_info = self.pocket_info['popularity_red_pocket'][0]
        join_requirement = pop_pocket_info.get('join_requirement')  # 需要的粉丝等级 1 为1级
        awards = pop_pocket_info.get('awards')  # 总价值
        start_time = pop_pocket_info.get('start_time')
        end_time = pop_pocket_info.get('end_time')
        last_time = pop_pocket_info.get('last_time')  # 持续时间
        remove_time = pop_pocket_info.get('remove_time')
        replace_time = pop_pocket_info.get('replace_time')
        current_time = pop_pocket_info.get('current_time')
        wait_num = pop_pocket_info.get('wait_num')  # 疑似第几个红包0为当前红包
        total_price = pop_pocket_info.get('total_price')
        sub_gift_li = []  # 礼物列表
        for sub_gift in awards:
            num = sub_gift['num']
            gift_name = sub_gift['gift_name']
            sub_gift_li.append([num, gift_name])
        dt1 = datetime.datetime.fromtimestamp(timestamp)
        dt2 = datetime.datetime.fromtimestamp(remove_time)
        diff = dt2 - dt1  # 计算时间差
        leave_time = diff.total_seconds()
        yield_pocketinfo = [leave_time, join_requirement, wait_num, total_price, sub_gift_li, self.cur_url,
                            self.block]  # 剩余时间、等级需要、等待第几个红包、总价值、礼物列表,地址、分区
        if join_requirement > 1:  # 如果要求的等级高 或者红包不是当前红包 则略过
            return
        else:
            return yield_pocketinfo

    def get_tianxuan(self):
        tianxuan_info = self.pocket_info['anchor']
        award_price_text = tianxuan_info.get('award_price_text')  # 礼物名字价值
        award_name = tianxuan_info.get('award_name')
        award_num = tianxuan_info.get('award_num')  # 总共几份
        leave_time = tianxuan_info.get('time')
        require_value = tianxuan_info.get('require_value')  # 对等级的限制值为0则没有限制
        yield_tianxuaninfo = [leave_time, require_value, award_price_text, award_name, award_num, self.cur_url,
                              self.block]  # 剩余时间、等级需求、价值、礼物名称、数量,地址、分区
        if require_value > 0 or '电池' not in award_price_text:  # 如果限制等级则略过
            return
        else:
            return yield_tianxuaninfo
