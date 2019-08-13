# -*- coding: utf-8 -*-

from pymongo import MongoClient
from scrapy.conf import settings
from scrapy import log


# 爬取的数据存入mongodb数据库
class GanjiPipeline(object):
    def __init__(self):
        connection = MongoClient(
            settings['MONGODB_SERVER'],
            settings['MONGODB_PORT']
        )
        db = connection[settings['MONGODB_DB']]
        self.collection = db[settings['MONGODB_COLLECTION']]

    def process_item(self, item, spider):
        self.collection.insert(dict(item))
        # log.msg('question added to mongodb database!',
        #         level=log.DEBUG, spider=spider)
        return item
