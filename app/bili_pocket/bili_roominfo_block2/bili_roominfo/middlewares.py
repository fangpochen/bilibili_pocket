# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals

# useful for handling different item types with a single interface
from itemadapter import is_item, ItemAdapter

def get_cookies_dict():
    cookies_str = "buvid3=90EADCE7-749E-0E67-0421-9B161EC62B6267771infoc; b_nut=1668864467; _uuid=E9436614-CB9F-1B2A-4C5C-4AB510BF23FB367669infoc; buvid4=6DE1ACFE-2B8D-2536-0F48-0DAC4B03E33469187-022111921-KrU2p7hQ0ITllS54oJlIsA%3D%3D; buvid_fp_plain=undefined; nostalgia_conf=-1.txt; CURRENT_FNVAL=4048; rpdid=|(mmJ)m)u~k0J'uYY))YRYJ~; i-wanna-go-back=-1.txt; LIVE_BUVID=AUTO3416689545716296; hit-new-style-dyn=0; hit-dyn-v2=1.txt; b_ut=5; home_feed_column=5; CURRENT_PID=3d032de0-d489-11ed-897c-8149aa219e74; theme_style=light; share_source_origin=COPY; FEED_LIVE_VERSION=V8; header_theme_version=CLOSE; CURRENT_QUALITY=0; bsource=search_google; innersign=0; browser_resolution=1920-503; b_lsid=D791B10AA_189E463C36A; fingerprint=68b69261dd0f6f8d1f9e8c8e35e39ef8; SESSDATA=e6f080fa%2C1707308519%2Cd193b%2A82Q-rW2A2newMOBP5tQXEXul2yZ8FEq4BLHNNgJ3kk-ZW5x2aKVMHkMFPKL5SBpM48eeMLzwAAFAA; bili_jct=048866c106a2d900045153a3385d6b5d; DedeUserID=3537115512047620; DedeUserID__ckMd5=36b31bda1e1bd839; sid=pqx4r7me; buvid_fp=68b69261dd0f6f8d1f9e8c8e35e39ef8; PVID=11"
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

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
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
