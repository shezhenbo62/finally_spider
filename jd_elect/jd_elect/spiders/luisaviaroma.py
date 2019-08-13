# -*- coding: utf-8 -*-
import scrapy
from jd_elect.items import JdElectItem
from urllib import parse
import re
import datetime
from urllib import parse
from fake_useragent import UserAgent


class KaolaSpider(scrapy.Spider):
    name = 'luisa'
    allowed_domains = ['www.luisaviaroma.com']
    start_urls = ['https://www.luisaviaroma.com/zh-cn/shop/%E7%94%B7%E5%A3%AB?lvrid=_gm_s',
                  'https://www.luisaviaroma.com/zh-cn/shop/%E5%A5%B3%E5%A3%AB?lvrid=_gw_s',
                  'https://www.luisaviaroma.com/zh-cn/shop/%E7%94%B7%E5%AD%A9?lvrid=_gkb_s',
                  'https://www.luisaviaroma.com/zh-cn/shop/%E5%A5%B3%E5%AD%A9?lvrid=_gkg_s',
                  'https://www.luisaviaroma.com/zh-cn/shop/%E5%AE%B6%E5%B1%85?lvrid=_ge_s',
                  ]
    ua = UserAgent()

    def start_requests(self):
        cookies = {
            'bm_sz': 'C8A9C2DF4A979D3A8A9A3CDA8F710E1F~YAAQsZcRYCiY67NpAQAA2v9AtAOEW8BGcqLjaN0Fek0hfxcffgXBW2Ksmpi8EmC2ovDk9JGHfRyeAgJlCtBO1jsDqc0QmQRrZe/VB1mSFTd46f5fanuhA3AF+ocY2MabcOICPKIOskJVL9CI0y4U67aAmjhSbo3xptHAuoX0rZSgOYZHy+CNoeiE9Uo04COneRAK7yz/',
            '_abck': 'CD8C11EDD4AECED963B9AC0BA65F93C5601197B11B7C000018A4985CA08CC93D~0~kJ2jIbZGflGa8rL7CHY+dTTtAxoPXVSlNnivsaHsiFM=~-1~-1',
            'LVR_UserData': 'Ver=6&cty=CN&curr=EUR&vcurr=CNY&lang=ZH',
            'LVR_User': 'ver=1',
            'LVR_Ref': 'faurl=aHR0cDovL3d3dy5sdWlzYXZpYXJvbWEuY29tL0NhdGFsb2cuYXNweD9MYW5nPVpIJkdlbmRlcj1tZW4mU2Vhc29uPXNhbGUmQ291bnRyeT1DTiZwYWdlPTEmYWpheD1mYWxzZSZsdnJpZD1fZ21fcyZha2FfcmU9MQ==&laurl=aHR0cDovL3d3dy5sdWlzYXZpYXJvbWEuY29tL1VzZXJTZXNzaW9uLmFzcHg/dj0yMDE5MDMxODE0NTAyOA==&fadate=2019-03-25 10:48:37&ladate=2019-03-25 11:33:25&faip=120.43.200.73&laip=121.207.105.73',
            'bm_mi': '99C9B0EA849641DA60D49B6D0982CD44~6aUtN5P3MFUxEi11mPuCSJrar9Lkx8q1Hgh5sEuDHEX/agrziw98N9WWLVzgtoo9BMRzzazYowJ6yXHxMhn/Bza3xbY/DoWsF9JNTFCU1/bPf04ZKi0dknWMpuxfIwbxaQtGRq572AsfsiP60aHWZvRBC1k7yQ86e/SA34B3oOjLnz6EOw5HSHPEfBujkQ9Gz+hqTBgTue2NU3VCDw1K7rFXzKrIBRkXhwok+2ThBUvrHPi26jG2JqZWQy60bj/0eK4EaMFk6ghjYBC+4BD50/JXlVBnK8vEr5zmjROXMfI=',
            'bm_sv': 'D54614042D5FF293CC11BE58393F1566~p6yzZxkhYIuidClZV2vGK/zvsGK5SZINlX0SPYHCEDqjM8V2YtfcEOMQp0tZm7bTj96fDfujm/HYiLVjNeTPdLM7aGuxvA7GsA6f5kiIKHUIW6CgTGutAnV8QnIHVRo2iseH+y/Y8ee2VRAoDkPzoAYHnGDvv5dQOAj96E2jzpI=',
            'LVR_MarketingCookies': 'true',
            'LVR_AnalyticsCookies': 'true',
            '_dy_ses_load_seq': '76521%3A1553510056435',
            '_dy_c_exps': '',
            '_dy_soct': '351053.574999.1553507358*351053.575000.1553510044*246797.371038.1553510056*246798.371039.1553510056*246799.371040.1553510056*246800.371041.1553510056*357258.590110.1553510056*135768.190303.1553510056*319900.614228.1553510057',
            'tc_scoring_pv': '9',
            'LVR_BC': 'viewed',
            '_dyid': '-4904419640465644514',
            '_dycst': 'dk.w.f.ws.',
            '_dy_geo': 'CN.AS.CN_FJ.CN_FJ_Fuzhou',
            '_dy_df_geo': 'China..Fuzhou',
            '_dy_toffset': '-1',
            '_dycnst': 'dg',
            'TCID': '2019311749208561787947',
            '_ga': 'GA1.2.515612354.1553507363',
            '_gid': 'GA1.2.1376282211.1553507363',
            'RT': 'sl=3&ss=1553510037855&tt=4297&obo=2&sh=1553510058369%3D3%3A2%3A4297%2C1553510058342%3D2%3A1%3A4297%2C1553510042154%3D1%3A0%3A4297&dm=www.luisaviaroma.com&si=f8f9cef4-68a7-47ba-8c0c-444afa241628&bcn=%2F%2F17d98a5a.akstat.io%2F&ld=1553510058369',
            'LVR_TRACKING': '1e07f7a5-a4dd-4723-b6fe-dea6f76ba703',
            '_dy_c_att_exps': '',
            'tc_cj_v2': '%5Ecl_%5Dny%5B%5D%5D_mmZZZZZZKOOMOJQMSJSNNZZZ%5D',
            'LVR_FT': 'viewed',
            'stc114797': 'tsa:1553507372083.1118127711.4087584.41160866984469824:20190325101932|env:1%7C20190425094932%7C20190325101932%7C1%7C1043009:20200324094932|uid:1553507372082.1557860242.718471.114797.1195089224.:20200324094932|srchist:1043009%3A1%3A20190425094932:20200324094932',
            'LVR_Touchpoint': 'url=/zh-cn/shop/%e5%a5%b3%e5%a3%ab$query=lvrid=_gw_s$referrer=https://www.luisaviaroma.com/zh-cn/?aka_sh=1&aka_re=1',
            'ak_bmsc': '971DC8CD325B23AB31C8201B9B0CAE8A17D4033E2670000099AE985CEDBE6730~plsO9XbXcwPoe1dwUrAfIesMnk3yaba4PSBFIyEXrZQdUHTuGbvqr988xhTrGsXaRv0DiX99Ovypu4yOB96cZ9L08vjSEfvGDesAss9KVrkfkuXdbz4iNo2h7HiSKJpdBPfplNSbLKm3MXOKW5TkFk/kbdcjAbnE3fGilpwQ4JCVebeLmORWVf1x0pKFcQIKZvmN6oaqPfCCcWzxuhT92XsfYs4jxpzgtM3RsBCepSwH/HjG5Ds1X14ukzqZYFX4UM',
            'ASP.NET_SessionId': 'jscmx4yvoneesvk2yp2u0nxl',
            '_dy_csc_ses': 't',
            'TCSESSION': '2019311834173409723508',
            '_dyjsession': '1bb41c09ade34caa8324dcf5468452a9',
        }

        for url in self.start_urls:
            yield scrapy.Request(url,
                                 callback=self.parse,
                                 cookies=cookies)

    def parse(self, response):
        item = JdElectItem()
        a_list = response.xpath("//div[@id='div_lp_body']//a")
        for a in a_list:
            item['brand_name'] = a.xpath("./span/span[@itemprop='brand']/span/text()").extract_first()
            item['title'] = a.xpath("./span/span[@itemprop='name']/text()").extract_first()
            item['goods_url'] = a.xpath("./@href").extract_first()
            if item['goods_url']:
                item['goods_url'] = 'https://www.luisaviaroma.com' + item['goods_url']
            item['img_url'] = a.xpath("./span/span[@class='picture']/span/img[1]/@data-src").extract_first()
            if item['img_url']:
                item['img_url'] = 'https:' + item['img_url']
            else:
                item['img_url'] = a.xpath("./span/span[@class='picture']/span/img[1]/@src").extract_first()
                item['img_url'] = parse.urljoin(response.url, item['img_url'])
            item['price'] = a.xpath("./span/span[@class='catalog__item__price price']/span/span[last()]/span/text()").extract_first()
            if item['price']:
                item['price'] = re.findall(r'(\d+)', item['price'])[0]
            item['discount'] = a.xpath("./span/span[@class='catalog__item__price price']/span/span[last()-1]/text()").extract_first()
            if item['discount']:
                item['discount'] = re.findall(r'(\d+%)', item['discount'])[0]
            item['price_ref'] = a.xpath("./span/span[@class='catalog__item__price price']/span/span[1]/text()").extract_first()
            if item['price_ref']:
                item['price_ref'] = re.findall(r'(\d+)', item['price_ref'])[0]
            item['create_time'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            yield item
