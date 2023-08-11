import datetime
import os
import subprocess
import sys
import time

from scrapy.cmdline import execute


def start_collect_pocket():
    while True:
        os.chdir(os.path.dirname(os.path.abspath(__file__)))
        sys.path.append(os.path.dirname(os.path.abspath(__file__)))
        try:
            print(datetime.datetime.now())
            execute(['scrapy', 'crawl', 'roominfo_b2'])
            # subprocess.call(['scrapy', 'crawl', 'roominfo_b2'])
        except SystemExit as e:
            print("Scrapy process exited with code:", e.code)
        # time.sleep(10)


if __name__ == '__main__':
    start_collect_pocket()
