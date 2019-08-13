# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html

from fake_useragent import UserAgent
import random

class RandomUserAgent(object):
    def process_request(self,request,spider):
        useragent = UserAgent()
        ua = useragent.chrome
        request.headers['UserAgent'] = ua

class ProxyMiddleware(object):
    def process_request(self,request,spider):
        proxy_list = ['http://47.98.234.177:3128','http://124.237.83.14:53281']
        proxy = random.choice(proxy_list)
        request.meta['proxy'] = proxy

class CheckProxy(object):
    def process_response(self,request,response,spider):
        print(request.meta['proxy'])
        return response