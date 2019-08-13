# -*- coding: utf-8 -*-
import scrapy
import re


class YoujiSpider(scrapy.Spider):
    name = 'youji'
    allowed_domains = ['www.mafengwo.cn']
    start_urls = ['http://www.mafengwo.cn/gonglve/']

    def parse(self, response):
        div_list = response.xpath("@div[class='feed-item _j_feed_item']")
        for div in div_list:
            item = {}
            item['title'] = div.xpath(".//div[@class='title']/text()").extract_first()
            item['info'] = div.xpath(".//div[@class='info']/text()").extract_first()
            item['dianzan_num'] = div.xpath(".//span[@class='num']/text()").extract_first()
            item['author'] = div.xpath(".//span[@class='author']/text()").extract_first()
            item['read_num'] = div.xpath(".//span[@class='nums']/text()").extract_first()
            item['href'] = div.xpath("./a/@href")
            yield scrapy.Request(item['href'],
                                 callback=self.parse_detail,
                                 meta={"item":item})

        # next_page = re.findall(r'data-page="(\d+)"',response.body.decode())[0]
        # next_page = dict(page=next_page)
        #
        # yield scrapy.FormRequest(
        #     "http://www.mafengwo.cn/gonglve/",
        #     formdata=next_page,
        #     callback=self.parse,
        #     # meta={"item": item}
        # )

    def parse_detail(self,response):
        item = response.meta['item']
        comment_list = response.xpath("//li[contains(@class,'clearfix comment_item')]")
        for comment in comment_list:
            item['comment'] = comment.xpath(".//div[@class='com-cont']/text()").extract_first()
            yield item
