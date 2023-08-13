# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html
import time 
import random

from scrapy import signals
# useful for handling different item types with a single interface
from itemadapter import is_item, ItemAdapter

def get_cookies_dict():
    cookies_str = "buvid3=90EADCE7-749E-0E67-0421-9B161EC62B6267771infoc; b_nut=1668864467; _uuid=E9436614-CB9F-1B2A-4C5C-4AB510BF23FB367669infoc; buvid4=6DE1ACFE-2B8D-2536-0F48-0DAC4B03E33469187-022111921-KrU2p7hQ0ITllS54oJlIsA%3D%3D; buvid_fp_plain=undefined; nostalgia_conf=-1; CURRENT_FNVAL=4048; rpdid=|(mmJ)m)u~k0J'uYY))YRYJ~; theme_style=light; i-wanna-go-back=-1; LIVE_BUVID=AUTO3416689545716296; hit-new-style-dyn=0; hit-dyn-v2=1; b_ut=5; home_feed_column=5; CURRENT_PID=3d032de0-d489-11ed-897c-8149aa219e74; theme_style=light; share_source_origin=COPY; FEED_LIVE_VERSION=V8; header_theme_version=CLOSE; CURRENT_QUALITY=0; bsource=search_google; fingerprint=8bae937410920dc95812411a74338e24; innersign=0; bili_jct=9d21775af8aa7d7e85f23afb33f88586; DedeUserID=1625760333; DedeUserID__ckMd5=1d58475273c83513; sid=hnlzhlng; buvid_fp=8bae937410920dc95812411a74338e24; PVID=2; b_lsid=EA1015DDD_189DFC40077; browser_resolution=1920-503"
    cookies_dict = {}
    for item in cookies_str.split('; '):
        key,value = item.split('=', maxsplit=1)
        cookies_dict[key] = value
    return cookies_dict

COOKIES_DICT = get_cookies_dict()

class BiliRoominfoSpiderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, or item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Request or item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info("Spider opened: %s" % spider.name)


class BiliRoominfoDownloaderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.
    def __init__(self) -> None:
        self.delay_times = 1

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # print('downloadmidware 触发')
        self.delay_times +=1
        if self.delay_times%30 == 0:
            # print(self.delay_times,'触发休息等待，等待3-5s')
            time.sleep(3)
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        request.cookies = COOKIES_DICT  # 加入cookies信息
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info("Spider opened: %s" % spider.name)

