# -*- coding: utf-8 -*-
import scrapy
import re
from copy import deepcopy
from selenium import webdriver


class MTSpider(scrapy.Spider):
    name = 'meituan'
    allowed_domains = ['meituan.com/']
    start_urls = ['https://wh.meituan.com/']

    def parse(self, response):
        li_list = response.xpath("//div[@class='category-nav-content-wrapper']/ul/li")
        for li in li_list:
            item = {}
            item['b_title'] = li.xpath(".//a/text()").extract_first()
            item['href'] = li.xpath(".//a/@href").extract_first()
            yield scrapy.Request(item['href'],
                                 dont_filter=True,
                                 callback=self.get_shop_list,
                                 meta={'item':deepcopy(item)})

    def get_shop_list(self, response):
        item = response.meta['item']
        driver = webdriver.PhantomJS("D:/chromedriver/phantomjs-2.1.1-windows/bin/phantomjs.exe")
        driver.get(item['href'])
        li_list = driver.find_elements_by_xpath("//ul[@class='list-ul']/li")
        for li in li_list:
            item['shop_name'] = li.find_element_by_xpath("./div[@class='info']/a/h4").text
            item['s_href'] = li.find_element_by_xpath("./div[@class='info']/a").get_attribute('href')
            item['sorce'] = li.find_element_by_xpath("./div[@class='info']/a/div/p").text
            item['comment_count'] = li.find_element_by_xpath("./div[@class='info']/a/div/p/span").text
            item['address'] = li.find_element_by_xpath("./div[@class='info']/a/p").text
            item['person_argv'] = li.find_element_by_xpath("./div[@class='info']/a/p/span").text
            yield scrapy.Request(item['s_href'],
                                 dont_filter=True,
                                 callback=self.get_detail_info,
                                 meta={'item':deepcopy(item)})

    def get_detail_info(self,response):
        item = response.meta['item']
        item['phone'] = re.findall(r'"phone":"(.*?)","openTime',response.body.decode('utf8','ignore'))
        print(item)
        yield item