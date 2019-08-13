# coding:utf-8

import requests
import hashlib
from lxml import etree
import threading
from queue import Queue
import time, time, json, random, re
from fake_useragent import UserAgent
import pandas as pd

ua = UserAgent()


# 解析线程类
class Parse(threading.Thread):
    # 初始化属性

    def __init__(self, number, data_list, req_thread, req_list):
        super(Parse, self).__init__()
        self.number = number  # 线程编号
        self.data_list = data_list  # 数据队列
        self.req_thread = req_thread  # 请求线程列表，为了判断采集线程存活状态
        self.is_parse = True  # 判断是否从数据队列里提取数据
        # self.category = category
        self.req_list = req_list

    def run(self):
        print('启动%d号解析线程' % self.number)
        # 无限循环，
        while True:
            # 如何判断解析线程的结束条件
            for t in self.req_thread:  # 循环所有采集线程
                if t.is_alive():  # 判断线程是否存活
                    break
            else:  # 如果循环完毕，没有执行break语句，则进入else
                if self.data_list.qsize() == 0:  # 判断数据队列是否为空
                    self.is_parse = False  # 设置解析为False

            # 判断是否继续解析
            if self.is_parse:  # 解析
                try:
                    data = self.data_list.get(timeout=3)  # 从数据队列里提取一个数据
                except Exception as e:  # 超时以后进入异常
                    data = None
                # 如果成功拿到数据，则调用解析方法
                if data is not None:
                    self.parse(data)  # 调用解析方法
            else:
                break  # 结束while 无限循环
        print('退出%d号解析线程' % self.number)

    # 页面解析函数
    def parse(self, data):
        html = etree.HTML(data)
        div_list = html.xpath("//div[@class='products']/div/div")
        content_list = []
        for div in div_list:
            # category_name
            brand_name = div.xpath("./div/a[1]/text()")[0] if len(div.xpath("./div/a[1]/text()")) > 0 else None  # 品牌名
            title = div.xpath("./div/a[2]/text()")[0] if len(div.xpath("./div/a[2]/text()")) > 0 else None  # 标题
            link = div.xpath("./a/@href")[0] if len(div.xpath("./a/@href")) > 0 else None  # 详情页链接
            final_price = float(div.xpath(".//p[@class='price red']/span/text()")[0].replace('¥', '').replace(',', '').replace('from', '').strip())\
                if len(div.xpath(".//p[@class='price red']/span/text()"))>0\
                else 0 # 最终价格
            original_price = float(div.xpath(".//p[@class='wasPrice']/span/text()")[0].replace('¥', '').replace(',', '').replace('from', '').strip())\
                if len(div.xpath(".//p[@class='wasPrice']/span/text()"))>0\
                else 0  # 原价
            offers = original_price - final_price  # 优惠金额
            if final_price != 0:
                discount = round(final_price/original_price, 2)
            else:
                discount = 1
            # rmb_price = goods.get('reference_price')  # 折合人民币价格
            # metric_score = goods.get('metric_score')  # 评分
            # sales = goods.get('sales')  # 销量
            # total_sales = goods.get('total_sales')  # 总销量
            content_list.append([brand_name, title, link, final_price, original_price, offers, discount])

        # 翻页
        next_url = html.xpath("//div[@class='pagination top']//li[@class='next item active']/a/@href")[0] if\
            len(html.xpath("//div[@class='pagination top']//li[@class='next item active']/a/@href")) > 0 else None
        if next_url is not None:
            self.req_list.put(next_url)
            print(content_list)
            pd_brand = pd.DataFrame(content_list, columns=['brand_name', 'title', 'link', 'final_price',
                                                           'original_price', 'offers', 'discount'])
            pd_brand.to_csv("C:/Users/Administrator/Desktop/selfridges.csv", index=False, mode='a', header=False)


# 采集信息类
class Crawl(threading.Thread):
    # 初始化
    def __init__(self, number, req_list, data_list):
        # 调用Thread 父类方法
        super(Crawl, self).__init__()
        # 初始化子类属性
        self.number = number
        self.req_list = req_list
        self.data_list = data_list
        self.headers = {'Connection': 'keep-alive',
                        'Cache-Control': 'max-age=0',
                        'Upgrade-Insecure-Requests': '1',
                        'User-Agent': ua.random,
                        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
                        'Referer': 'http://www.selfridges.com/CN/zh/',
                        'Accept-Encoding': 'gzip, deflate',
                        'Accept-Language': 'zh-CN,zh;q=0.9',
                        # 'Cookie': '_ga=GA1.2.1483854218.1543819054; COOKIE_NOTICE_SEEN=seen; CoreID6=72238359665815438190549&ci=90262645; SIGNUP_POPUP_SEEN=seen; SF_COUNTRY_LANG=CN_zh; WC_PERSISTENT=kEY5al0K%2bsSh2WfHJH6%2bxkN1rC8%3d%0a%3b2019%2d02%2d20+02%3a03%3a31%2e086%5f1550628211083%2d221308%5f10052%5f%2d1002%2c%2d1%2cCNY%5f10052; _gid=GA1.2.1507110988.1551345684; utag_chan={"channel":"","channel_set":"","channel_converted":false}; __atuvc=1%7C8%2C2%7C9; Apache=10.77.3.197.1551404825831171; JSESSIONID=0000rrR2ojigDOjtlKVcNgJpoNH:188k091sd; WC_SESSION_ESTABLISHED=true; WC_ACTIVEPOINTER=%2d1%2c10052; WC_USERACTIVITY_-1002=%2d1002%2c10052%2cnull%2cnull%2cnull%2cnull%2cnull%2cnull%2cnull%2cnull%2cCdOQmL%2fCozFYHJEbRqx0G7TaOjtTyEdumhEKiYK48UYCaV9yG4ICmzFOkLYe7eXWDzO3fDXG4ZcE%0aLEMun%2bFtv6QBC7CGZHcYAF2ij4lXYUNmiX6jRGWimfmp3ZXabtGR%2f9A9WA%2fYKW0wnlrBTI%2bRjPl%2b%0ajbHKUMSqYf9CiyCd3t76ERByxvbuspXKZ5Mmo5yurD7AGQ%3d%3d; WC_GENERIC_ACTIVITYDATA=[7443677480%3atrue%3afalse%3a0%3aSz%2bGVxUc4ATFiVgKfY5a5qyhBXw%3d][com.ibm.commerce.context.globalization.GlobalizationContext|%2d1%26CNY%26%2d1%26CNY][com.ibm.commerce.context.experiment.ExperimentContext|null][com.ibm.commerce.context.audit.AuditContext|null][com.ibm.commerce.context.base.BaseContext|10052%26%2d1002%26%2d1002%26%2d1][CTXSETNAME|Store][com.ibm.commerce.catalog.businesscontext.CatalogContext|16151%26null%26false%26false%26false][com.ibm.commerce.context.entitlement.EntitlementContext|4000000000000000008%264000000000000000008%26null%26%2d2000%26null%26null%26null]; cmTPSet=Y; CM_PROD_CATS=6990092|573379,IB_6990092|N; _gat_tealium=1; BIGipServer~S603887-RD2~WWW_HTTP_POOL=!f+Br91EFirGeF082mi3gewpiRYKC98ROQHTSMchgoPigtAu+OzgtjI+yOPWhYeH4CLc+hNtHrbraQhkg/PQ4y0lOYmnMjvkBC7CCP0w=; mmapi.store.p.0=%7B%22mmparams.d%22%3A%7B%7D%2C%22mmparams.p%22%3A%7B%22pd%22%3A%221582942665506%7C%5C%22-1174486384%7CmwAAAApVAwANdZ%2B2AhGZKQABEQABQm0rHV4PAJ1WqRfsndZI%2Bk7LzOlY1kgAAAAA%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F8ABkRpcmVjdAFZEQIAAgAAAAAAAACEtwAAhbcAAIS3AAACAJHsAADAHGKalyARAP%2F%2F%2F%2F8BIBFYEf%2F%2FBAAAAQAAAAABJlgCAMj6AgAA3wUBAFZ9%2BSS3UREA%2F%2F%2F%2F%2FwFREVoR%2F%2F8YAAABAAAAAAEIkgIAoUEDAAAAAAAAAAFF%5C%22%22%2C%22srv%22%3A%221582942665509%7C%5C%22lvsvwcgeu04%5C%22%22%7D%7D; mmapi.store.s.0=%7B%22mmparams.d%22%3A%7B%7D%2C%22mmparams.p%22%3A%7B%7D%7D; 90262645_clogin=l=1551404826&v=1&e=1551408465528; utag_main=v_id:016772c94b76000dca810bbdaf000306e002006600bd0$_sn:10$_ss:0$_st:1551408465699$_pn:7%3Bexp-session$ses_id:1551404825683%3Bexp-session'
                        }

    # 线程启动的时候调用
    def run(self):
        # 输出启动线程信息
        print('启动采集线程%d号' % self.number)
        # 如果请求队列不为空，则无限循环，从请求队列里拿请求url
        while self.req_list.qsize() > 0:
            # 从请求队列里提取url
            url = self.req_list.get()
            print('%d号线程采集：%s' % (self.number, url))
            # 防止请求频率过快，随机设置阻塞时间
            time.sleep(round(random.uniform(0, 1), 2))
            # 发起http请求，获取响应内容，追加到数据队列里，等待解析
            response = requests.get(url, headers=self.headers)
            if response.status_code == 200:
                self.data_list.put(response.content.decode("utf-8"))  # 向数据队列里追加

    # def get_proxy(self):
    #     return requests.get('http://119.23.203.63:6066/get/').content


def main():
    # 设置线程数量
    concurrent = 3
    conparse = 3
    # 生成请求队列
    req_list = Queue()
    # 生成数据队列 ，请求以后，响应内容放到数据队列里
    data_list = Queue()
    # # 创建互斥锁
    # lock = threading.Lock()
    # 构建网页分类编号列表
    url_list = ['http://www.selfridges.com/CN/zh/cat/mens/on_sale/?cm_sp=MegaMenu-_-men-_-Sale',
                'http://www.selfridges.com/CN/zh/cat/womens/on_sale/?cm_sp=MegaMenu-_-Women-_-Sale']
    # 循环生成多个请求url
    for base_url in url_list:
        # 加入请求队列
        req_list.put(base_url)

    # 生成N个采集线程
    req_thread = []
    for i in range(concurrent):
        t1 = Crawl(i + 1, req_list, data_list)  # 创造线程
        t1.setDaemon(True)
        t1.start()
        req_thread.append(t1)

    # 生成N个解析线程
    parse_thread = []
    for i in range(conparse):
        t2 = Parse(i + 1, data_list, req_thread, req_list)  # 创造解析线程
        t2.setDaemon(True)
        t2.start()
        parse_thread.append(t2)
    for t in req_thread:
        t.join()
    for t in parse_thread:
        t.join()


if __name__ == '__main__':
    main()
