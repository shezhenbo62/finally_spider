# -*- coding: utf-8 -*-
import scrapy
import re
from copy import deepcopy
from brooksbrothers.items import BrooksbrothersItem


class BrooksSpider(scrapy.Spider):
    name = 'brooks'
    allowed_domains = ['www.brooksbrothers.com']
    start_urls = ['http://www.brooksbrothers.com/womens/women,default,sc.html/']

    def parse(self, response):
        li_list = response.xpath("//div[@class='categorylandingpage-left-navigation-defaultlayout']/div/ul/li")
        for li in li_list:
            b_href = li.xpath("./a/@href").extract_first()
            yield scrapy.Request(b_href,
                                 callback=self.get_detail_url)

    def get_detail_url(self,response):
        div_list = response.xpath("//div[@class='product-name']")
        for div in div_list:
            item = BrooksbrothersItem()
            item['s_href'] = 'https://www.brooksbrothers.com' + div.xpath(".//a/@href").extract_first()
            yield scrapy.Request(item['s_href'],
                                 callback=self.get_product_info,
                                 meta={'item': deepcopy(item)})

        next_url = response.xpath("//a[@class='page-next page-nav-btn']/@href").extract_first()
        if next_url:
            yield scrapy.Request(next_url,
                                 callback=self.get_detail_url,
                                 meta={'item': item})

    def get_product_info(self,response):
        item = response.meta['item']
        div_list = response.xpath("//div[@class='wrapper-product-details col-xs-12 clearfix']")
        for div in div_list:
            item['title'] = div.xpath(".//h1[@class='product-name']/text()").extract_first()
            item['desc'] = div.xpath(".//p[@class='description']/text()").extract_first()
            item['img_url'] = div.xpath(".//ul[@class='pdp-thumbnails']/li/a/img/@src").extract()
            color = re.findall(r'Color=(.*?)&amp;dwvar',response.body.decode('utf-8'))
            size = re.findall(r'title="size : (.*?)"',response.body.decode('utf-8'))
            id =re.findall(r"id: '(.*?)',",response.body.decode('utf-8'))[0]
            for i in color:
                for j in size:
                    item['sku'] = id + '_'*5 + i + '_' + j + '_'*7
                    sku_url = 'https://www.brooksbrothers.com/'+item['title']+'/'+item['sku']+',default,pd.html'
                    yield scrapy.Request(sku_url,
                                         callback=self.get_sku_info,
                                         meta={'item':deepcopy(item)})

    def get_sku_info(self,response):
        item = response.meta['item']
        price = response.xpath(".//span[@class='price-value']/text()").extract_first()
        item['product_price'] = '$' + price
        print(item)
        yield item



