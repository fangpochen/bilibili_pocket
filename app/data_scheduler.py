import os
from datetime import datetime, timedelta
from random import randint

from app import db
from app.models import Phone, Pocket, Tian, Room
from app.mysql_util import save_list

pocket = 'None'

USER_AGENTS = [
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1.txt; SV1; AcooBrowser; .NET CLR 1.txt.1.txt.4322; .NET CLR 2.0.50727)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)",
    "Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.5; AOLBuild 4337.35; Windows NT 5.1.txt; .NET CLR 1.txt.1.txt.4322; .NET CLR 2.0.50727)",
    "Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1.txt; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
    "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.txt.0.3705; .NET CLR 1.txt.1.txt.4322)",
    "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.txt.1.txt.4322; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 3.0.04506.30)",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1.txt; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.3 (Change: 287 c9dfb30)",
    "Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.6",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1.txt; en-US; rv:1.txt.8.1.txt.2pre) Gecko/20070215 K-Ninja/2.1.txt.1.txt",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1.txt; zh-CN; rv:1.txt.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0",
    "Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Kazehakase/0.4.5",
    "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.txt.9.0.8) Gecko Fedora/1.txt.9.0.8-1.txt.fc10 Kazehakase/0.5.6",
    "Mozilla/5.0 (Windows NT 6.1.txt; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 Safari/535.20",
    "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; fr) Presto/2.9.168 Version/11.52",
]
BALL_URL = 'http://nba.titan007.com/jsData/matchResult/{}.js?version=2023101022'


class Config(object):
    JOBS = [
        # {
        #     'id': 'job1',
        #     'func': 'app.data_scheduler:collect_pocket',
        #     'trigger': 'interval',  # 指定任务触发器 interval
        #     # 'hour': 15,
        #     'seconds': 10
        # },
        # {
        #     'id': 'job2',
        #     'func': 'app.data_scheduler:collect_room_id',
        #     'trigger': 'interval',  # 指定任务触发器 interval
        #     'minutes': 30
        # },
        {
            'id': 'job3',
            'func': 'app.data_scheduler:delete_expired_room_info',
            'trigger': 'interval',  # 指定任务触发器 interval
            'seconds': 5
        },
        # {
        #     'id': 'job4',
        #     'func': 'app.data_scheduler:get_size_data',
        #     'trigger': 'cron',  # 指定任务触发器 interval
        #     'hour': 15,
        #     'minute': 10
        # }
    ]


RANDOM_AGENT = USER_AGENTS[randint(0, len(USER_AGENTS) - 1)]
HEADERS = {
    'Referer': 'http://nba.titan007.com/cn/League/2021-2022/36.html',
    'User-Agent': RANDOM_AGENT
}


# 获取txt文本
def change_phone_number():  # 一个函数，用来做定时任务的任务。
    pwd = os.getcwd() + '\phone\\'
    files = os.listdir(pwd)
    update_time = datetime.now()

    for i in files:
        phone_arr = []
        with open(pwd + i) as f:
            lines = f.readlines()
            url = lines[-2].replace('\n', '')
            end_time = lines[-1]
            end_time = datetime.strptime(end_time, '%Y-%m-%d %H:%M:%S')
            print(url)
            print(end_time)
            lines = lines[0:-2]
            for line in lines:
                space_index = line.find(' ')
                phone = line[space_index + 1:space_index + 12]
                phone_data = Phone(phone=phone,
                                   url=url,
                                   state=0,
                                   update_time=update_time,
                                   end_time=end_time)
                print(phone)
                phone_arr.append(phone_data)
        save_list(phone_arr)


# def collect_pocket():
#     crawl_threads = Process(target=start_collect_pocket)
#     crawl_threads.start()
#     crawl_threads.join()
#     print(1111111111111111)


# def collect_room_id():
#     start_collect_room_id()


def delete_expired_room_info():
    try:
        now_time = datetime.now()
        previous_time = now_time - timedelta(hours=24)
        db.session.query(Phone).filter(now_time < Phone.end_time, Phone.update_time < previous_time).update(
            {Phone.state: 0})
        db.session.query(Pocket).filter(now_time > Pocket.end_time).delete()
        db.session.query(Tian).filter(now_time > Tian.end_time).delete()
        db.session.query(Room).filter(now_time > Room.end_time).delete()
        db.session.commit()
        db.session.close()
    except Exception as e:
        print(e)


if __name__ == '__main__':
    change_phone_number()
    # collect_pocket()
    # get_home_data()
    # delete_expired_room_info()
