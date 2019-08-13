# _*_ coding:utf-8 _*_
from fake_useragent import UserAgent
import requests
from multiprocessing import Pool
from lxml import etree
import re
import time, pymongo, datetime
import pandas as pd
from requests.packages.urllib3.exceptions import InsecureRequestWarning
# 禁用安全请求警告
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


def time_decorator(run):
    def func(*args, **kwargs):
        start_time = time.time()
        run(*args, **kwargs)
        end_time = time.time()
        print('抓取耗时%s秒' % (end_time-start_time))
    return func


class TmSpider(object):
    def __init__(self):
        # self.start_url = 'https://list.tmall.com/search_product.htm?q={}&type=p&vmarket=&spm=875.7931836%2FB.a2227oh.d100&from=mallfp..pc_1_searchbutton'
        self.start_url = 'https://list.tmall.com/search_product.htm?q={}&type=p&vmarket=&spm=875.7931836%2FB.a2227oh.d100&from=mallfp..pc_1_searchbutton'
        self.headers = {'User-Agent': ua.random,
                        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
'accept-encoding': 'gzip, deflate, br',
'accept-language': 'zh-CN,zh;q=0.9',
'cache-control': 'max-age=0',
'cookie': 'cna=r5cTFAVzS0gCAXFo2mWr3FNi; hng=CN%7Czh-CN%7CCNY%7C156; lid=%E5%A5%BD%E7%9A%84%E4%BA%8B%E6%83%85lv; _med=dw:1920&dh:1080&pw:1920&ph:1080&ist:0; t=2729faefaec453f12677acb9bf00eeb1; tracknick=%5Cu597D%5Cu7684%5Cu4E8B%5Cu60C5lv; _tb_token_=38ee417345e87; cookie2=1fc8050bc06957c06a56085e310aad4a; _m_h5_tk=b4b31bd321ac4ec11f0f6a07a5d00810_1553077430349; _m_h5_tk_enc=ee713e35d3a6307dba2d24f27838bb6c; cq=ccp%3D1; tt=tmall-main; res=scroll%3A1903*5499-client%3A1903*943-offset%3A1903*5499-screen%3A1920*1080; pnm_cku822=098%23E1hvzvvUvbpvUvCkvvvvvjiPRLMvzjDERsLh6jljPmPy6j1nR2cWzjEhRL5W6jtWKphv8hCvvvvvvhCvphvwv9vvp%2F1vpCQmvvChNhCvjvUvvhBZphvwv9vvBHoivpvUphvhiZ05NLkEvpvVpyUUCC%2BwmphvLhxUU9mFe160O9NBZBh7Ectz8SoxdX%2BaneUndXZzh7QEVA1lYb8raAidoxZlimEkLkx%2Flj7JnBr%2FVA1laB4qNB9fb5cGeCl1pVQ4S4ZCvpvVphhvvvvv2QhvCvvvMMGtvpvhphvvv8wCvvBvpvpZ; l=bBSKZQvcvo9cS8zxBOCNSuI8U0bOxIRAguPRwd4yi_5LK1xY8z_OltZUbev6Vj5R_u8p4qzKRqp9-etk9; isg=BKGhn2CaWeFQmvII2omLDEVBsG175heciD2PXAN2nagFasE8S54lEM-oyNjJoq14',
'referer': 'https://www.tmall.com/',
'upgrade-insecure-requests': '1'}

    def parse(self, url):
        # s.keep_alive = False
        # s.adapters.DEFAULT_RETRIES = 5
        try:
            response = requests.get(url, headers=self.headers, verify=False, timeout=10)
        except Exception as e:
            print(e)
            time.sleep(1)
            self.parse(url)
        else:
            try:
                return response.content.decode('gbk')
            except Exception as f:
                print(f)
                return None

    @staticmethod
    def get_content_info(response, brand, category):
        html = etree.HTML(response)
        div_list = html.xpath("//div[@class='product  ']")
        content_list = []
        for div in div_list:
            item = {}
            item['category'] = category
            item['brand_name'] = brand
            goods_url = div.xpath(".//p[@class='productTitle']/a/@href")
            if len(goods_url) == 0:
                goods_url = div.xpath(".//div[@class='productImg-wrap']/a/@href")
            item['pc_goods_url'] = 'https:' + goods_url[0]
            item['phone_goods_url'] = 'https://detail.m.tmall.com/item.' + goods_url[0].split('.')[3]
            item['img_url'] = 'https:'+div.xpath(".//img/@src")[0] if len(div.xpath(".//img/@src"))>0 else None
            item['z_price'] = div.xpath(".//p[@class='productPrice']/em/text()")[0] if len(div.xpath(".//p[@class='productPrice']/em/text()"))>0 else None
            item['shop_name'] = div.xpath(".//p[@class='productStatus']/span[3]/@data-nick")[0] if len(div.xpath(".//p[@class='productStatus']/span[3]/@data-nick"))>0 else None
            if item['shop_name'] is None:
                data = div.xpath(".//a[@class='productShop-name']")[0]
                item['shop_name'] = data.xpath("string(.)").strip()
            item['sale_count'] = div.xpath(".//p[@class='productStatus']/span[1]/em/text()")[0] if len(div.xpath(".//p[@class='productStatus']/span[1]/descendant-or-self::*/text()"))>0 else None
            item['comment_count'] = div.xpath(".//p[@class='productStatus']/span[2]/a/text()")[0] if len(div.xpath(".//p[@class='productStatus']/span[2]/descendant-or-self::*/text()"))>0 else None
            content_list.append(item)
        next_url = html.xpath("//a[@class='ui-page-s-next']/@href")[0] if len(html.xpath("//a[@class='ui-page-s-next']/@href"))>0 else None
        if next_url is not None:
            next_url = 'https://list.tmall.com/search_product.htm' + next_url
            # print(next_url)
        return content_list, next_url

    def get_detail_info(self, detail_rsp, content, info_list):
        # print(detail_rsp)
        html = etree.HTML(detail_rsp)
        content['title'] = html.xpath("//div[@class='main cell']/text()")[0].strip() if len(html.xpath("//div[@class='main cell']/text()"))>0 else None
        content['activity'] = re.findall(r'"content":\["(.*?)"\],', detail_rsp)[0] if len(re.findall(r'"content":\["(.*?)"\],', detail_rsp))>0 else None
        content['z_price_ref'] = html.xpath("//div[@class='module-price']//span/text()")[0] if len(html.xpath("//div[@class='module-price']//span/text()"))>0 else None
        content['create_time'] = datetime.date.today().strftime('%Y-%m-%d')
        self.save_content_list(content)
        return info_list

    @staticmethod
    def save_content_list(result):
        MONGO_URL = 'localhost'
        MONGO_DB = 'haitao'
        MONGO_TABLE = 'tianmao'
        client = pymongo.MongoClient(MONGO_URL)
        db = client[MONGO_DB]
        try:
            if db[MONGO_TABLE].insert(result):
                print('存储到mongodb成功', result)
        except Exception as e:
            print(e)
            print('存储到mongodb失败', result)

    @time_decorator
    def run(self):
        p = Pool(processes=10)
        client = pymongo.MongoClient('localhost', 27017)
        db = client['brand']
        D88_brand = db['D88_brand']
        data = pd.DataFrame(list(D88_brand.find()))
        data = data.drop(columns=['_id'])
        data = data.values.tolist()
        for info in data:
            brand = info[0]
            category = info[1]
            next_url = self.start_url.format(brand)
            info_list = []
            while next_url:
                response = self.parse(next_url)
                if response is not None:
                    content_list, next_url = self.get_content_info(response, brand, category)
                    print(next_url)
                    for content in content_list:
                        # time.sleep('%.2f' % random.random())
                        detail_rsp = p.apply_async(self.parse, args=(content['phone_goods_url'],))
                        detail_rsp = detail_rsp.get()
                        detail_info = self.get_detail_info(str(detail_rsp), content, info_list)
        p.close()
        p.join()


if __name__ == '__main__':
    ua = UserAgent()
    tm_spider = TmSpider()
    tm_spider.run()
