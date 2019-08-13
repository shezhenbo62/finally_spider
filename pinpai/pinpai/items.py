# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class PinpaiItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    brand_name = scrapy.Field()
    brand_country = scrapy.Field()
    brand_url = scrapy.Field()
    c_name = scrapy.Field()
    en_name = scrapy.Field()
