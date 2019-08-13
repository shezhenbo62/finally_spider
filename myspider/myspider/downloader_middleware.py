from fake_useragent import UserAgent


class RandomUserAgentMiddleWare(object):
    """
    随机更换User-Agent
    """
    def __init__(self, crawler):
        super(RandomUserAgentMiddleWare, self).__init__()
        self.ua = UserAgent()
        self.ua_type = crawler.settings.get("RANDOM_UA_TYPE", "random")

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler)

    def process_request(self, request, spider):
        def get_ua_type():
            return getattr(self.ua, self.ua_type)   # 取对象 ua 的 ua_type 的这个属性, 相当于 self.ua.self.ua_type

            # request.meta["proxy"] = "ip:port" 设置代理

        # random_useragent = get_ua_type()
        request.headers.setdefault('User-Agent', get_ua_type())