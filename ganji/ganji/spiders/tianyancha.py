# -*- coding: utf-8 -*-
import scrapy


class TianyanSpider(scrapy.Spider):
    name = 'tyc'
    allowed_domains = ['tianyancha.com']
    start_urls = ['https://www.tianyancha.com/login']

    def parse(self, response):
        post_data = dict(autoLogin='true',
                         cdpassword="ce48da32d97cfe328acf5bf477c0a45b",
                         loginway="PL",
                         mobile="15102768455")
