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

    def __init__(self, number, data_list, req_thread, category, req_list):
        super(Parse, self).__init__()
        self.number = number  # 线程编号
        self.data_list = data_list  # 数据队列
        self.req_thread = req_thread  # 请求线程列表，为了判断采集线程存活状态
        self.is_parse = True  # 判断是否从数据队列里提取数据
        self.category = category
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
        goods_list = data.get('results')
        category_name = data.get('breadcrumb').get('paths')[0].get('name')
        content_list = []
        for goods in goods_list:
            brand_name = goods.get('brand_name')  # 品牌名
            title = goods.get('name')  # 标题
            link = 'https://cn.pharmacyonline.com.au/product/' + goods.get('url_path')
            final_price = goods.get('final_price')  # 最终价格
            original_price = goods.get('price')  # 原价
            discount = round(final_price/original_price, 2)
            offers = original_price - final_price  # 优惠金额
            rmb_price = goods.get('reference_price')  # 折合人民币价格
            metric_score = goods.get('metric_score')  # 评分
            sales = goods.get('sales')  # 销量
            total_sales = goods.get('total_sales')  # 总销量
            content_list.append([category_name, brand_name, title, link, final_price, original_price, offers, discount,
                                 rmb_price, metric_score, sales, total_sales])
        page = data.get('pagination').get('current').get('page') + 1
        category_id = data.get('breadcrumb').get('paths')[0].get('key')
        next_url = 'https://cn.pharmacyonline.com.au/queryapi/lists?page={}&cid={}&sort=top'.format(page, category_id)
        if content_list != []:
            self.req_list.put(next_url)
            print(content_list)
            pd_brand = pd.DataFrame(content_list, columns=['category_name', 'brand_name', 'title', 'link', 'final_price',
                                                           'original_price', 'offers', 'discount', 'rmb_price',
                                                           'metric_score', 'sales', 'total_sales'])
            pd_brand.to_csv("C:/Users/Administrator/Desktop/pharmacy.csv", index=False, mode='a', header=False)


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
                        'X-Requested-With': 'XMLHttpRequest',
                        'User-Agent': ua.random,
                        'Accept': 'application/json, text/javascript, */*; q=0.01',
                        'Referer': 'https://cn.pharmacyonline.com.au/category/7435.html',
                        'Accept-Encoding': 'gzip, deflate, br',
                        'Accept-Language': 'zh-CN,zh;q=0.9',
                        'Cookie': 'bfd_tmd=d31519076b7f1e2a5b06865ed6349ea0.54018148.1541749668000; bfd_tma=d31519076b7\
                        f1e2a5b06865ed6349ea0.61354798.1541749668000; _uuid=08824350-33F9-4A70-BF8F-5262C5B66B9A;\
                         sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%22166f770fc11fe-0632d596e82593-37664109-2073\
                         600-166f770fc12485%22%2C%22%24device_id%22%3A%22166f770fc11fe-0632d596e82593-37664109-2073600-\
                         166f770fc12485%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%\
                         A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_referrer%22%3A%22%22%2C%22%24latest_referrer_host%22%3A\
                         %22%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6\
                         %8E%A5%E6%89%93%E5%BC%80%22%7D%7D; gray_u=40598699; __sonar=2231550784603877616; CACHED_FRONT\
                         _FORM_KEY=GlSjMMqcUtfo305R; _wtag=10052.25.18; Hm_lvt_a3a5d79d073a1c3f23a74df6bc6a6c2c=1551253\
                         416; cart_item_count=0; frontend=109trjhvo4b8tl39ukn5erdsq1; customerId=; bfd_sid=4bfbe0ea94f9\
                         211b2902a60fb2830c84; cartItemCount=0; loginRet=10; Hm_lpvt_a3a5d79d073a1c3f23a74df6bc6a6c2c=1\
                         551258115'}

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
                self.data_list.put(response.json())  # 向数据队列里追加


def main():
    # 设置线程数量
    concurrent = 3
    conparse = 3
    # 生成请求队列
    req_list = Queue()
    # 生成数据队列 ，请求以后，响应内容放到数据队列里
    data_list = Queue()
    # 构建网页分类编号列表
    category = [6435, 6472, 6653, 6603, 6705]
    # 循环生成多个请求url
    for i in category:
        base_url = 'https://cn.pharmacyonline.com.au/queryapi/lists?page=1&cid=%s&sort=top' % i
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
        t2 = Parse(i + 1, data_list, req_thread, category, req_list)  # 创造解析线程
        t2.setDaemon(True)
        t2.start()
        parse_thread.append(t2)
    for t in req_thread:
        t.join()
    for t in parse_thread:
        t.join()


if __name__ == '__main__':
    main()
