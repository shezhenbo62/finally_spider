# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html

from fake_useragent import UserAgent
import random


class RandomUserAgentMiddlewares(object):
    def process_request(self, request, spider):
        useragent = UserAgent()
        ua = useragent.chrome
        request.headers['UserAgent'] = ua


class ProxyMiddleware(object):
    def process_request(self, request, spider):
        proxy_list = ['http://101.110.119.59:80','http://219.141.153.12:80','http://42.236.123.17:80']
        proxy = random.choice(proxy_list)
        request.meta['proxy'] = proxy
