# -*- coding: utf-8 -*-
import scrapy


class PengpaiSpiderSpider(scrapy.Spider):
    name = 'pengpai_spider'
    allowed_domains = ['www.thepaper.cn']
    start_urls = ['https://www.thepaper.cn/']

    def parse(self, response):
        div_list = response.xpath("//div[@class='news_li']")
        for div in div_list:
            item = {}
            item['title'] = div.xpath("./h2/a/text()").extract_first()
            item['detail'] = div.xpath("./p/text()").extract_first()
            item['author'] = div.xpath("./div[@class='pdtt_trbs']/a/text()").extract_first()
            item['release_time'] = div.xpath("./div[@class='pdtt_trbs']/span[1]/text()").extract_first()
            item['comment_num'] = div.xpath("./div[@class='pdtt_trbs']/span[last()]/text()").extract_first()
            yield item