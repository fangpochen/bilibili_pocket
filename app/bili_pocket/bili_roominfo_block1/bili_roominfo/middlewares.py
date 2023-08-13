# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html
import random

from scrapy import signals


# useful for handling different item types with a single interface


def get_cookies_dict():
    cookies0 = "buvid3=D984F467-20F8-4F14-A8CA-3B5CDAF670F336764infoc; LIVE_BUVID=AUTO7416917572375433; _uuid=771024E39-E94D-10889-10F1E-2EBD1FAFAB5C38680infoc; buvid4=DE1558E2-C5FF-A9E5-930F-640E25672A2238079-023081120-sMnbBmv8ix9EZp+BvA6l6g%3D%3D; fingerprint=68b69261dd0f6f8d1f9e8c8e35e39ef8; buvid_fp_plain=undefined; SESSDATA=12520f6c%2C1707309265%2Cf9656%2A81kcMppgM3z10zMuylzXS0Qz2AOpGGdMsw85kwgJVTEodwBhXbGfCzue9BgJYxEzTtc1jhdQAAIQA; bili_jct=2af5ee1276850b58e4e7f1653941ce21; DedeUserID=1625760333; DedeUserID__ckMd5=1d58475273c83513; sid=padngzew; buvid_fp=68b69261dd0f6f8d1f9e8c8e35e39ef8; innersign=0; b_nut=100; i-wanna-go-back=-1; b_ut=5; bsource=search_baidu; header_theme_version=CLOSE; home_feed_column=5; browser_resolution=1920-931; nostalgia_conf=-1; b_lsid=CDEC4F105_189EE3D40E0; PVID=4"
    cookies1 = "buvid3=37C8CE99-A312-B6BB-5EFA-A7EF522441DA43138infoc; b_nut=1691926043; buvid4=6B67899B-BB73-CB45-C00B-BC5858DC245743138-023081319-nVDPmcrgLsqV74Y95VpMWQ%3D%3D; b_lsid=FFBFA817_189EEA6A0E7; innersign=0; _uuid=EC1092FD9-7FBA-4E98-467A-A352DFA513A247002infoc; header_theme_version=CLOSE; home_feed_column=5; browser_resolution=1920-419; buvid_fp=68b69261dd0f6f8d1f9e8c8e35e39ef8; LIVE_BUVID=AUTO9616919260825722; SESSDATA=b434b4ef%2C1707478131%2Cb46b7%2A81bo7x8mjDNyrRfT5o_vpVMOiTcOIjqS30Jx7PB52EPwhN0F4hsVu4w-fUPpXZaIhhsT_ceAAAIQA; bili_jct=2c3897034c8384bb0d7e03c7905fd9a4; DedeUserID=1625760333; DedeUserID__ckMd5=1d58475273c83513; sid=ewb99d1a; PVID="
    cookies2 = "buvid3=37C8CE99-A312-B6BB-5EFA-A7EF522441DA43138infoc; b_nut=1691926043; buvid4=6B67899B-BB73-CB45-C00B-BC5858DC245743138-023081319-nVDPmcrgLsqV74Y95VpMWQ%3D%3D; b_lsid=FFBFA817_189EEA6A0E7; innersign=0; _uuid=EC1092FD9-7FBA-4E98-467A-A352DFA513A247002infoc; header_theme_version=CLOSE; home_feed_column=5; buvid_fp=68b69261dd0f6f8d1f9e8c8e35e39ef8; LIVE_BUVID=AUTO9616919260825722; PVID=2; bp_video_offset_1625760333=829307590147047424; SESSDATA=8dc03e7a%2C1707478708%2C27888%2A81_uFlO0oeJUlFjO-WktFr5PhHYHwunLZQ2gDBFNJQvNOeYNfq1doU05ip-guY1P3pIMGPtQAAFAA; bili_jct=fb453d9760fb8af59dfdffa7ab9c07ce; DedeUserID=3537115512047620; DedeUserID__ckMd5=36b31bda1e1bd839; sid=6l6i6vr3; browser_resolution=1920-419"
    cookies3 = "buvid3=7565192F-855D-8C5F-4D30-A485211699C324554infoc; b_nut=1684857824; _uuid=21101119F-11110-53E9-4F76-1096BC103E6109124896infoc; i-wanna-go-back=-1; header_theme_version=CLOSE; FEED_LIVE_VERSION=V8; CURRENT_FNVAL=4048; rpdid=0zbfvS7M31|Fo8G4tIe|4aY|3w1QqnxT; buvid4=76619598-990D-5128-977E-7C64B8C106B525237-023052400-cJA8FXQvRy62lL6KWqpEksSPM4t5k39KY%2FbiKiDg73cEppXsCigxQg%3D%3D; LIVE_BUVID=AUTO1716908171008515; fingerprint=2ded7c6fc121501be6d63837a158e2c7; buvid_fp_plain=undefined; bili_jct=8422c83aac67469f0a55230a5b7d1487; DedeUserID=289406780; DedeUserID__ckMd5=e263b7e70648a323; buvid_fp=2ded7c6fc121501be6d63837a158e2c7; CURRENT_QUALITY=116; b_ut=5; bili_ticket=eyJhbGciOiJFUzM4NCIsImtpZCI6ImVjMDIiLCJ0eXAiOiJKV1QifQ.eyJleHAiOjE2OTIxNzgyMDgsImlhdCI6MTY5MTkxOTAwOCwicGx0IjotMX0.QJnfir7rASMNVzjtDxPO-MhetA9aETC-JJME_qbx-O1UfLsWyS_dDDCqDc9wm4MP0jzEsDig8V4_PpOYsJ8fY9h2bHUnO7aFyV6EjcQ-MUOhFXHdl-FvtqyAjbuXAhCc; bili_ticket_expires=1692178208; b_lsid=8AAF688C_189EE6D77BE; bp_video_offset_289406780=829288421714296851; sid=6l7t7qr3; innersign=0; PVID=1; home_feed_column=4; browser_resolution=427-948"
    cookies4 = "buvid3=EC7839C2-9651-5604-6CC3-6AC05A0AF4D913560infoc; b_nut=1691852513; i-wanna-go-back=-1; b_ut=7; _uuid=A6EC3E62-FE58-6FC2-D2D9-3A4C651210C4914418infoc; buvid_fp=1435cf234a3f0fc7f17cbb17af046022; buvid4=E5AA09CD-DF98-F094-12E9-F886B048945F14776-023081223-b1nz50QSFWA2lGX%2BFti0iA%3D%3D; bili_jct=8b444eed94a76c5c7479452c0583e22a; DedeUserID=1638153913; DedeUserID__ckMd5=5389b4fa208da72b; sid=7arjmb7f; innersign=0; b_lsid=E38A8E97_189EEB4F773; header_theme_version=CLOSE; home_feed_column=4; browser_resolution=1399-718"
    cookies5 = "buvid3=A27CD387-5B08-74D3-A9FC-C489D3E7BC3024546infoc; b_nut=1666028924; bsource=search_baidu; _uuid=8835E2FB-C63B-6157-10D7D-753C474E628539798infoc; buvid4=9F692412-D49C-84EA-5B56-4597EE5F958626020-022101801-zOesG7u/uucsujF4N3niBw%3D%3D; i-wanna-go-back=-1; fingerprint=9b6a63e6aeb0a1adc11cc77fa70f9a7c; buvid_fp_plain=undefined; fingerprint3=6763eeaf74ff593a8134a3f22eda176e; buvid_fp=9b6a63e6aeb0a1adc11cc77fa70f9a7c; hit-dyn-v2=1; b_ut=5; CURRENT_QUALITY=80; nostalgia_conf=-1; CURRENT_BLACKGAP=0; CURRENT_FNVAL=4048; hit-new-style-dyn=0; rpdid=|(mmJ)m)|~u0J'uY~Jk~uk|); innersign=0; b_lsid=B769A1C3_189EEB1AE6E; theme_style=light; header_theme_version=CLOSE; home_feed_column=5; SESSDATA=0883dc6c%2C1707479712%2C5b1bb%2A81xpVoOAaN_UJGenElaK5bIALFMPfoT-DwxVC201bh2UYca7OGskMZNZ0CpeYxrwdEKLj9uAAACQA; bili_jct=5c4fe081736382e25b15c995654c0fb5; DedeUserID=1375248909; DedeUserID__ckMd5=94859f7dd2de49f4; sid=5w8qjcm6; browser_resolution=1920-464; LIVE_BUVID=AUTO8816919277284735; PVID=2"
    cookie_arr = [cookies0, cookies1, cookies2, cookies3, cookies4, cookies5]
    random_cookie = random.choice(cookie_arr)
    cookies_dict = {}
    for item in random_cookie.split('; '):
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
