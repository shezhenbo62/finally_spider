# -*- coding: utf-8 -*-
import scrapy
from guazi.items import GuaziItem
from copy import deepcopy

class GzescSpider(scrapy.Spider):
    name = 'gzesc'
    allowed_domains = ['guazi.com']
    start_urls = ['https://www.guazi.com/wh/buy/']

    def start_requests(self):
        cookies = {"antipas":"G82915765Sty661fj8938K19146"}
        # cookies = {i.split("=")[0]:i.split("=")[1] for i in cookies.split("; ")}
        # headers = {"Cookie":cookies}
        yield scrapy.Request(
            self.start_urls[0],
            callback=self.parse,
            cookies=cookies,
            # dont_filter=True
            # headers = headers
        )

    def parse(self, response):
        cookies = {"antipas": "G82915765Sty661fj8938K19146"}
        li_list = response.xpath("//div[@class='dd-all clearfix js-brand js-option-hid-info']/ul/li")
        for li in li_list:
            item = GuaziItem()
            # item = {}
            item['brand'] = li.xpath("./p/a/text()").extract_first()
            item['s_href'] = 'https://www.guazi.com' + li.xpath("./p/a/@href").extract_first()
            yield scrapy.Request(item['s_href'],
                                 callback=self.parse_car_info,
                                 cookies=cookies,
                                 meta={'item': deepcopy(item)})

    def parse_car_info(self,response):
        item = deepcopy(response.meta['item'])
        cookies = {"antipas": "G82915765Sty661fj8938K19146"}
        li_list = response.xpath("//ul[@class='carlist clearfix js-top']/li")
        for li in li_list:
            item['title'] = li.xpath("./a/h2/text()").extract_first()
            item['img_url'] = li.xpath("./a/img/@src").extract_first()
            item['detail_url'] = 'https://www.guazi.com' + li.xpath("./a/@href").extract_first()
            item['price'] = li.xpath(".//div[@class='t-price']/p/text()").extract_first() + '万'
            yield scrapy.Request(item['detail_url'],
                                 callback=self.parse_car_detail,
                                 cookies=cookies,
                                 meta={'item': deepcopy(item)})

        #下一页
        next_url = 'https://www.guazi.com' + response.xpath("//span[text()='下一页']/../@href").extract_first()
        if next_url is not None:
            yield scrapy.Request(next_url,
                                 callback=self.parse_car_info,
                                 meta={'item': item})

    def parse_car_detail(self,response):
        item = response.meta['item']
        span_list = response.xpath("//dl[@class='people-infor clearfix']/dt/span")
        for span in span_list:
            item['people_info'] = span.xpath("./text()").extract_first()
            yield item
