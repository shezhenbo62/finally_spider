# -*- coding: utf-8 -*-
import scrapy
from pinpai.items import PinpaiItem


class PpSpider(scrapy.Spider):
    name = 'pp'
    allowed_domains = ['www.chinapp.com']
    start_urls = 'https://www.chinapp.com/'

    def start_requests(self):
        yield scrapy.Request(self.start_urls,dont_filter=True,callback=self.parse)

    def parse(self, response):
        good_list = response.xpath("//div[@class='wrapNav']/ul/li[9]/div//ul/li/a[1]")

        for good in good_list:
            item = PinpaiItem()
            good_url = good.xpath("./@href").extract_first()
            if good_url:
                good_url = "https://www.chinapp.com" + good_url
                yield scrapy.Request(
                    good_url,
                    callback=self.good_detial,
                    meta={"item": item})

    def good_detial(self,response):
        item = response.meta["item"]
        d_list = response.xpath("//ul[@class='dqDeilList']/li")
        for d in d_list:
            d_url = d.xpath(".//div[@class='dqLeftImg']/a/@href").extract_first()
            if d_url:
                d_url = "https://www.chinapp.com" + d_url
                yield scrapy.Request(
                    d_url,
                    callback=self.good_xiangqin,
                    meta={"item": item})

        next_url = response.xpath("//a[text()='下一页']/@href").extract_first()
        if next_url is not None:
            next_url = "https://www.chinapp.com" + next_url
            yield scrapy.Request(next_url,
                                 callback=self.good_detial,
                                 meta={'item': item})

    def good_xiangqin(self,response):
        item = response.meta["item"]
        item["brand_name"] = response.xpath("//div[@class='side_one']/p[2]/text()").extract_first()
        en_name = response.xpath("//div[@class='side_one']/p[3]/label[text()='外文名称：']").extract_first()
        if en_name is None:
            item["brand_country"] = response.xpath("//div[@class='side_one']/p[4]/text()").extract_first()
            item["brand_url"] = response.xpath("//div[@class='side_one']/p[9]/text()").extract_first()
        else:
            item["brand_country"] = response.xpath("//div[@class='side_one']/p[5]/text()").extract_first()
            item["brand_url"] = response.xpath("//div[@class='side_one']/p[10]/text()").extract_first()
        yield item