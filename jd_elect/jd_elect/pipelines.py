# -*- coding: utf-8 -*-

from pymongo import MongoClient
from scrapy.conf import settings


# 爬取的数据存入mongodb数据库且根据url和activity去重
class KaoLaPipeline(object):
    def __init__(self):
        connection = MongoClient(
            settings['MONGODB_SERVER'],
            settings['MONGODB_PORT']
        )
        db = connection[settings['MONGODB_DB']]
        self.collection = db[settings['MONGODB_COLLECTION']]

    def process_item(self, item, spider):
        url_find = {'goods_url': item['goods_url']}
        if self.collection.find_one(url_find):
            old_activity = self.collection.find_one(url_find)['activity']
            if item['activity'] != old_activity:
                print("***************旧数据，但是活动更新***************\n{}".format(item))
                self.collection.update(url_find, {'$set': {"activity": item['activity'], "create_time": item['create_time']}})
        else:
            print("***************此条数据为更新数据***************\n{}".format(item))
            self.collection.insert(dict(item))
        return item


class JdElectPipeline(object):
    def __init__(self):
        connection = MongoClient(
            settings['MONGODB_SERVER'],
            settings['MONGODB_PORT']
        )
        db = connection[settings['MONGODB_DB']]
        self.collection = db[settings['MONGODB_COLLECTION']]

    def process_item(self, item, spider):
        url_find = {'goods_url': item['goods_url']}
        if self.collection.find_one(url_find):
            old_price = self.collection.find_one(url_find)['price']
            if float(item['price']) < float(old_price):
                print("***************旧数据，直接更新该数据***************\n{}".format(item))
                self.collection.update(url_find, {'$set': {"activity": item['activity'], "create_time": item['create_time']}})
        else:
            print("***************新数据，直接插入***************\n{}".format(item))
            self.collection.insert(dict(item))
        return item


class LuisaviaromaPipeline(object):
    def __init__(self):
        connection = MongoClient(
            settings['MONGODB_SERVER'],
            settings['MONGODB_PORT']
        )
        db = connection[settings['MONGODB_DB']]
        self.collection = db[settings['MONGODB_COLLECTION']]

    def process_item(self, item, spider):
        url_find = {'goods_url': item['goods_url']}
        if self.collection.find_one(url_find):
            old_price = self.collection.find_one(url_find)['price']
            if float(item['price']) < float(old_price):
                print("***************旧数据，直接删除后插入更新数据***************\n{}".format(item))
                self.collection.update(url_find, {'$set': {"activity": item['activity'], "create_time": item['create_time']}})
        else:
            print("***************新数据，直接插入***************\n{}".format(item))
            self.collection.insert(dict(item))
        return item