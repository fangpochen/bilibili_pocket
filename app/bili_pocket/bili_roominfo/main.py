import os
import sys

from scrapy.cmdline import execute


def start_collect_pocket():
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    try:
        execute(['scrapy', 'crawl', 'roominfo'])
    except SystemExit as e:
        print("Scrapy process exited with code:", e.code)

# if __name__ == '__main__':
#     start_collect_pocket()
