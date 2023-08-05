import os
import sys
import time

from scrapy.cmdline import execute


def start_collect_room_id():
    while True:
        os.chdir(os.path.dirname(os.path.abspath(__file__)))
        sys.path.append(os.path.dirname(os.path.abspath(__file__)))
        try:
            execute(['scrapy', 'crawl', 'roomid'])
        except SystemExit as e:
            print("Scrapy process exited with code:", e.code)
        time.sleep(1800)


if __name__ == '__main__':
    start_collect_room_id()
