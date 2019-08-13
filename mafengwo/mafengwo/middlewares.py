# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html
from fake_useragent import UserAgent

class RandomUserAgentMiddlewares:
    def process_request(self,request,spider):
        ua = UserAgent()
        useragent = ua.chrome
        request.headers["User-Agent"] = useragent

class CheckUserAgent:
    def process_response(self,request,response,spider):
        print(request.headers["User-Agent"])
        return response