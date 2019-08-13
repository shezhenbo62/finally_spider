# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class BrooksbrothersItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    s_href = scrapy.Field()
    title = scrapy.Field()
    desc = scrapy.Field()
    img_url = scrapy.Field()
    sku = scrapy.Field()
    product_price = scrapy.Field()
