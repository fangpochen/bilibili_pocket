from scrapy import signals
from scrapy.http import Request


class CookieMiddleware:
    def __init__(self, cookie_url):
        self.cookie_url = cookie_url

    @classmethod
    def from_crawler(cls, crawler):
        middleware = cls(cookie_url=crawler.settings.get('COOKIE_URL'))
        crawler.signals.connect(middleware.spider_opened, signal=signals.spider_opened)
        return middleware

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)
        self.update_cookie(spider)

    def update_cookie(self, spider):
        request = Request(self.cookie_url, callback=self.parse_cookie)
        spider.crawler.engine.crawl(request, spider)

    def parse_cookie(self, response, spider):
        new_cookie = response.headers.getlist('Set-Cookie')

        if new_cookie:
            cookie_dict = {}
            for cookie in new_cookie:
                key, value = cookie.decode('utf-8').split(';')[0].split('=')
                cookie_dict[key] = value.strip()

            spider.settings.set('COOKIES_ENABLED', True)
            spider.settings.set('COOKIES_DEBUG', True)
            spider.settings.set('COOKIES', cookie_dict)