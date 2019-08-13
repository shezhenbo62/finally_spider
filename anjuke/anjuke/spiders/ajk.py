# -*- coding: utf-8 -*-
import scrapy
from copy import deepcopy
import time


class AjkSpider(scrapy.Spider):
    name = 'ajk'
    allowed_domains = ['wuhan.anjuke.com']
    start_urls = ['https://wuhan.anjuke.com/sale/p1/']

    def parse(self, response):
        li_list = response.xpath("//ul[@id='houselist-mod-new']/li")
        item = {}
        for li in li_list:
            # item = {}
            item['title'] = li.xpath("./div[@class='house-details']/div/a/text()").extract_first()
            item['house_type'] = li.xpath(".//div[@class='details-item'][1]/span[1]/text()").extract_first()
            item['size'] = li.xpath(".//div[@class='details-item'][1]/span[2]/text()").extract_first()
            item['seller'] = li.xpath(".//div[@class='details-item'][1]/span[last()]/text()").extract_first()
            item['address'] = li.xpath(".//div[@class='details-item'][2]/span/text()").extract_first()
            item['price'] = li.xpath("./div[@class='pro-price']/span[1]/strong/text()").extract_first() + '万'
            item['detail_url'] =li.xpath("./div[@class='house-details']//a/@href").extract_first()
            yield scrapy.Request(item['detail_url'],
                                 callback=self.parse_detail,
                                 meta={'item': deepcopy(item)})

        next_url = response.xpath("//a[@class='aNxt']/@href").extract_first()
        if next_url is not None:
            yield scrapy.Request(next_url,
                                 callback=self.parse,
                                 meta={'item': deepcopy(item)})

    def parse_detail(self,response):
        item = response.meta['item']
        item['detail_comment'] = response.xpath("//div[@class='houseInfo-desc']//text()").extract_first()
        yield item