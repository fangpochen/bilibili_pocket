# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class BiliRoomInfoItem(scrapy.Item):
    pocket_info = scrapy.Field()
    room_block = scrapy.Field()
    room_id=  scrapy.Field()