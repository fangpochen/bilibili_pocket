# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html
from scrapy import signals
# useful for handling different item types with a single interface


def get_cookies_dict():
    cookies_str = "buvid3=D984F467-20F8-4F14-A8CA-3B5CDAF670F336764infoc; LIVE_BUVID=AUTO7416917572375433; _uuid=771024E39-E94D-10889-10F1E-2EBD1FAFAB5C38680infoc; buvid4=DE1558E2-C5FF-A9E5-930F-640E25672A2238079-023081120-sMnbBmv8ix9EZp+BvA6l6g%3D%3D; fingerprint=68b69261dd0f6f8d1f9e8c8e35e39ef8; buvid_fp_plain=undefined; SESSDATA=12520f6c%2C1707309265%2Cf9656%2A81kcMppgM3z10zMuylzXS0Qz2AOpGGdMsw85kwgJVTEodwBhXbGfCzue9BgJYxEzTtc1jhdQAAIQA; bili_jct=2af5ee1276850b58e4e7f1653941ce21; DedeUserID=1625760333; DedeUserID__ckMd5=1d58475273c83513; sid=padngzew; buvid_fp=68b69261dd0f6f8d1f9e8c8e35e39ef8; innersign=0; b_nut=100; i-wanna-go-back=-1; b_ut=5; bsource=search_baidu; header_theme_version=CLOSE; home_feed_column=5; browser_resolution=1920-931; nostalgia_conf=-1; b_lsid=CDEC4F105_189EE3D40E0; PVID=4"
    cookies_dict = {}
    for item in cookies_str.split('; '):
        key, value = item.split('=', maxsplit=1)
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
        # self.delay_times +=1
        # if self.delay_times%30 == 0:
        #     # print(self.delay_times,'触发休息等待，等待3-5s')
        #     time.sleep(3)
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


class ProxyDownloaderMiddleware:
    _proxy = ('o191.kdltps.com', '15818')

    def process_request(self, request, spider):
        # 用户名密码认证
        username = "t19190774262146"
        password = "7a00m1js"
        request.meta['proxy'] = "http://%(user)s:%(pwd)s@%(proxy)s/" % {"user": username, "pwd": password,
                                                                        "proxy": ':'.join(
                                                                            ProxyDownloaderMiddleware._proxy)}

        # 白名单认证
        # request.meta['proxy'] = "http://%(proxy)s/" % {"proxy": proxy}
        request.headers["Connection"] = "close"
        return None

    def process_exception(self, request, exception, spider):
        """捕获407异常"""
        if "'status': 407" in exception.__str__():  # 不同版本的exception的写法可能不一样，可以debug出当前版本的exception再修改条件
            from scrapy.resolver import dnscache
            dnscache.__delitem__(ProxyDownloaderMiddleware._proxy[0])  # 删除proxy host的dns缓存
        return exception
