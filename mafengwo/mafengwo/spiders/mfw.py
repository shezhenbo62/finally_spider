# -*- coding: utf-8 -*-
import scrapy
import re


class MfwSpider(scrapy.Spider):
    name = 'mfw'
    allowed_domains = ['mafengwo.cn']
    start_urls = ['http://passport.mafengwo.cn']

    def parse(self, response):
        post_data = dict(
            passport="15102768455",
            password="zy190688",
            code=''
        )
        yield scrapy.FormRequest(
            "https://passport.mafengwo.cn/login/",
            formdata=post_data,
            callback=self.user_center
        )

    def user_center(self,response):
        print(re.findall(r'马蜂窝',response.body.decode()))
        yield scrapy.Request(
            "http://www.mafengwo.cn/u/66318413.html",
            callback=self.parse_detial
        )

    def parse_detial(self, response):
        print(re.findall("佘振波", response.body.decode()))
