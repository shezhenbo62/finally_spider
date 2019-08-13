# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html

from fake_useragent import UserAgent
import base64


class RandomUserAgentMiddlewares(object):
    def process_request(self, request, spider):
        useragent = UserAgent()
        ua = useragent.chrome
        request.headers['UserAgent'] = ua


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