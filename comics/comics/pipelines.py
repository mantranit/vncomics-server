# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import pymongo
import os

class ComicsPipeline:
    def open_spider(self, spider):
        self.client = pymongo.MongoClient("mongodb://heroku_f1mzb91l:61ra6cfnh8lse8d1ju2quaq0n9@ds239557.mlab.com:39557/heroku_f1mzb91l?retryWrites=false")
        self.db = self.client.get_default_database()
        self.comics = self.db['comics']

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        row = self.comics.count_documents({u'name': item['name']})
        if row > 0:
            print("Already exists")
        else:
            self.comics.insert_one({
                u'name': item['name'],
                u'cover': item['cover'],
                u'url': item['url']
            })
        return item
