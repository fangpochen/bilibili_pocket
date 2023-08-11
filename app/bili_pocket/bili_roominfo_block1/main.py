import datetime
import os
import subprocess
import sys
import time


def start_collect_pocket():
    while True:
        os.chdir(os.path.dirname(os.path.abspath(__file__)))
        sys.path.append(os.path.dirname(os.path.abspath(__file__)))
        try:
            print(datetime.datetime.now())
            subprocess.call(['scrapy', 'crawl', 'roominfo_b1'])
        except SystemExit as e:
            print("Scrapy process exited with code:", e.code)
        # time.sleep(20)


if __name__ == '__main__':
    start_collect_pocket()
