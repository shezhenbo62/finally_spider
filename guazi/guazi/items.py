# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class GuaziItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    brand = scrapy.Field()
    s_href = scrapy.Field()
    title = scrapy.Field()
    img_url = scrapy.Field()
    detail_url = scrapy.Field()
    price = scrapy.Field()
    people_info = scrapy.Field()
