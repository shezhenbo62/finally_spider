# coding:utf-8

import random
import requests
import pandas as pd
import pymongo


def read_info():
    data = pd.read_excel('D:/fidder/request.xls')
    ua = pd.read_excel('D:/fidder/ua_string.xls')
    data = data.dropna(how='all')
    data = data.reset_index()
    data = data.drop(columns=['index', 'higo2'])
    return data.values.tolist(), ua.values.tolist()


def parse(data, ua_list):
    num = len(data)//7
    for i in range(num):
        item = {}
        ua = random.choice(ua_list)[0]
        headers = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
                   'Accept-Encoding': 'gzip, deflate',
                   'Accept-Language': 'zh-CN,zh;q=0.9',
                   'Cache-Control': 'max-age=0',
                   'Connection': 'keep-alive',
                   'Host': 'v.lehe.com',
                   'Upgrade-Insecure-Requests': '1',
                   'User-Agent': ua}
        split_list = data[i * 7][0].split(' ')
        url = 'http://v.lehe.com'+split_list[1]
        resp = requests.get(url, headers=headers).json()
        item['brand_name'] = resp.get('data').get('brand_info').get('name')
        item['brand_name_cn'] = resp.get('data').get('brand_info').get('name_cn')
        item['brand_story'] = resp.get('data').get('brand_info').get('brand_story')
        save_to_mongodb(item)


def save_to_mongodb(item):
    try:
        if db[MONGO_TABLE].insert(item):
            print('存储到mongodb成功', item)
    except Exception:
        print('存储到mongodb失败', item)


if __name__ == '__main__':
    MONGO_URL = 'localhost'
    MONGO_DB = 'brand_story'
    MONGO_TABLE = 'higo'
    client = pymongo.MongoClient(MONGO_URL)
    db = client[MONGO_DB]
    data, ua_list = read_info()
    parse(data, ua_list)
