# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:['http://219.150.189.212:9999', 'http://180.118.247.8:9000', 'http://121.232.148.138:9000']
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html

from fake_useragent import UserAgent
import random

class RandomUserAgentMiddlewares(object):
    def process_request(self,request,spider):
        useragent = UserAgent()
        ua = useragent.chrome
        request.headers['UserAgent'] = ua

class ProxyMiddleware(object):
    def process_request(self,request,spider):
        proxy_list = ['http://219.150.189.212:9999', 'http://180.118.247.8:9000', 'http://121.232.148.138:9000']
        proxy = random.choice(proxy_list)
        request.meta['proxy'] = proxy

class CheckProxy(object):
    def process_response(self,request,response,spider):
        print(request.meta['proxy'])
        return response