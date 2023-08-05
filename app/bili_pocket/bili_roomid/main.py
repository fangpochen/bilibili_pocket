import json
import os
import sys

from scrapy.cmdline import execute


def start_collect_room_id():
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    try:
        execute(['scrapy', 'crawl', 'roomid'])
    except SystemExit as e:
        print("Scrapy process exited with code:", e.code)


if __name__ == '__main__':
    start_collect_room_id()
