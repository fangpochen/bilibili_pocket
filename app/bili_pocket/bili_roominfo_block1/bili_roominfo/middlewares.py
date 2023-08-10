# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals

# useful for handling different item types with a single interface
from itemadapter import is_item, ItemAdapter

def get_cookies_dict():
    cookies_str = 'buvid3=7565192F-855D-8C5F-4D30-A485211699C324554infoc; b_nut=1684857824; _uuid=21101119F-11110-53E9-4F76-1096BC103E6109124896infoc; i-wanna-go-back=-1; header_theme_version=CLOSE; FEED_LIVE_VERSION=V8; CURRENT_FNVAL=4048; rpdid=0zbfvS7M31|Fo8G4tIe|4aY|3w1QqnxT; buvid4=76619598-990D-5128-977E-7C64B8C106B525237-023052400-cJA8FXQvRy62lL6KWqpEksSPM4t5k39KY%2FbiKiDg73cEppXsCigxQg%3D%3D; LIVE_BUVID=AUTO1716908171008515; fingerprint=2ded7c6fc121501be6d63837a158e2c7; buvid_fp_plain=undefined; bili_jct=8422c83aac67469f0a55230a5b7d1487; DedeUserID=289406780; DedeUserID__ckMd5=e263b7e70648a323; buvid_fp=2ded7c6fc121501be6d63837a158e2c7; CURRENT_QUALITY=116; b_ut=5; PVID=15; innersign=0; b_lsid=6F1051AB6_189DE39AC19; home_feed_column=4; browser_resolution=894-948'
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
