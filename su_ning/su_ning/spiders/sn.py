# -*- coding: utf-8 -*-
import scrapy
from su_ning.items import SuNingItem
import re
from copy import deepcopy


class SnSpider(scrapy.Spider):
    name = 'sn'
    allowed_domains = ['snbook.suning.com']
    start_urls = ['http://snbook.suning.com/web/trd-fl/999999/0.htm']

    def parse(self, response):
        li_list = response.xpath("//div[@id='sider_opr']//li[contains(@class,'lifirst')]")
        for li in li_list:
            item = SuNingItem()
            # item = {}
            item['big_title'] = li.xpath("./div[@class='second-sort']/a/text()").extract_first()
            item['small_title'] = li.xpath("./div[@class='three-sort']/a/text()").extract_first()
            item['href'] = 'http://snbook.suning.com' + li.xpath("./div[@class='three-sort']/a/@href").extract_first()
            item1 = deepcopy(item)
            yield scrapy.Request(item['href'],
                                 callback=self.parse_typepage,
                                 meta={'item': item1})

    def parse_typepage(self, response):
        # 获取下一页的地址http://snbook.suning.com/web/trd-fl/100301/46.htm?pageNumber=2&sort=0
        item = deepcopy(response.meta['item'])
        li_list = response.xpath("//ul[@class='clearfix']/li")
        for li in li_list:
            item['book_name'] = li.xpath(".//div[@class='book-title']/a/text()").extract_first()
            item['book_href'] = li.xpath(".//div[@class='book-title']/a/@href").extract_first()
            item['author'] = li.xpath(".//div[@class='book-author']/a/text()").extract_first()
            item['descrip'] = li.xpath(".//div[@class='book-descrip c6']/text()").extract_first()
            yield scrapy.Request(item['book_href'],
                                 callback=self.book_price_list,
                                 meta={'item':deepcopy(item)})

        # 下一页
        page_count = int(re.findall(r'var pagecount=(\d+);', response.body.decode())[0])
        current_page = int(re.findall(r'var currentPage=(\d+);',response.body.decode())[0])
        if current_page<page_count:
            next_url = item['href'] + '?pageNumber={}&sort=0'.format(current_page+1)
            yield scrapy.Request(next_url,
                                 callback=self.parse_typepage,
                                 meta={'item': item})

    def book_price_list(self, response):
        item = response.meta['item']
        pan_url = 'http://snbook.suning.com/web/ebook/checkPriceShowNew.do?bookId={}&completeFlag=2'
        img_url_list = response.xpath("//a[@class='btn shidu fl']/@onclick")
        for img_url in img_url_list:
            book_id = re.findall(r'/web/read/all/(\d+).htm', str(img_url))[0]
            price_url = pan_url.format(book_id)
            yield scrapy.Request(price_url,
                                 callback=self.get_book_price,
                                 meta={'item':item})

    def get_book_price(self, response):
        price_list = response.xpath("//em")
        for price in price_list:
            item = response.meta['item']
            item['price'] = price.xpath("./text()").extract_first()
            yield item
