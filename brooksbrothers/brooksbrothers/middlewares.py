from fake_useragent import UserAgent
import base64


class RandomUserAgentMiddlewares(object):
    def process_request(self, request, spider):
        useragent = UserAgent()
        ua = useragent.chrome
        request.headers['UserAgent'] = ua

# 代理服务器
proxyServer = "http://http-dyn.abuyun.com:9020"

# 代理隧道验证信息
proxyUser = "H66666O5CGR6WMKD"
proxyPass = "44FE751B898116AE"

proxyAuth = "Basic " + base64.urlsafe_b64encode(bytes((proxyUser + ":" + proxyPass), "ascii")).decode("utf8")

class ProxyMiddleware(object):
    def process_request(self, request, spider):
        request.meta["proxy"] = proxyServer

        request.headers["Proxy-Authorization"] = proxyAuth
