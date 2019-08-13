# -*- coding: utf-8 -*-
import scrapy
from pinpai.items import PinpaiItem


class PpSpider(scrapy.Spider):
    name = 'pclady'
    allowed_domains = ['https://cosme.pclady.com.cn/']
    start_urls = 'https://cosme.pclady.com.cn/brand_list.html'

    def start_requests(self):
        yield scrapy.Request(self.start_urls,dont_filter=True,callback=self.parse)

    def parse(self, response):
        good_list = response.xpath("//div[@class='part']//ul[@class='tagName clearfix']/li")
        for good in good_list:
            item = PinpaiItem()
            item['c_name'] = good.xpath("./a/span[1]/text()").extract_first()
            item['en_name'] = good.xpath("./a/span[2]/text()").extract_first()
            good_url = good.xpath("./a/@href").extract_first()
            if good_url:
                good_url = "https:" + good_url
                yield scrapy.Request(
                    good_url,
                    callback=self.good_detial,
                    dont_filter=True,
                    meta={"item": item})

    def good_detial(self,response):
        item = response.meta["item"]
        d_url = response.xpath("//div[@class='typeMode']/a[2]/@href").extract_first()
        if d_url:
            d_url = "https:" + d_url
            yield scrapy.Request(
                d_url,
                callback=self.good_xiangqin,
                dont_filter=True,
                meta={"item": item})

    def good_xiangqin(self,response):
        item = response.meta["item"]
        item['brand_country'] = response.xpath("//div[@class='topInfo']/p[4]/i/text()").extract_first()
        item['brand_url'] = response.xpath("////div[@class='topInfo']/p[@class='link']/a/text()").extract_first()
        yield item