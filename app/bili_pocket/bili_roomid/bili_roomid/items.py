# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

class BiliRoomIdItem(scrapy.Item):
    roomid = scrapy.Field()
    uid = scrapy.Field()
    roomblock =  scrapy.Field()

