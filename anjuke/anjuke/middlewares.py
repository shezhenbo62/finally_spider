# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html

from fake_useragent import UserAgent
import random
import base64

class RandomUserAgent(object):
    def process_request(self,request,spider):
        useragent = UserAgent()
        ua = useragent.chrome
        request.headers['UserAgent'] = ua

# class ProxyMiddleware(object):
#     def process_request(self,request,spider):
#         proxy_list = ['http://120.78.59.193:8080','http://101.227.5.36:9000','http://221.2.174.3:8060']
#         proxy = random.choice(proxy_list)
#         request.meta['proxy'] = proxy

# 代理服务器
proxyServer = "http://http-cla.abuyun.com:9030"

# 代理隧道验证信息
proxyUser = "H70FFCHS6574326C"
proxyPass = "CB4506D29AEECFAF"

proxyAuth = "Basic " + base64.urlsafe_b64encode(bytes((proxyUser + ":" + proxyPass), "ascii")).decode("utf8")

class ProxyMiddleware(object):
    def process_request(self, request, spider):
        request.meta["proxy"] = proxyServer

        request.headers["Proxy-Authorization"] = proxyAuth