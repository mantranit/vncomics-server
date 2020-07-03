# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import pymongo
import os
import re

class ComicsPipeline:

    def no_accent_vietnamese(self, s):
        s = re.sub(r'[àáạảãâầấậẩẫăằắặẳẵ]', 'a', s)
        s = re.sub(r'[ÀÁẠẢÃĂẰẮẶẲẴÂẦẤẬẨẪ]', 'A', s)
        s = re.sub(r'[èéẹẻẽêềếệểễ]', 'e', s)
        s = re.sub(r'[ÈÉẸẺẼÊỀẾỆỂỄ]', 'E', s)
        s = re.sub(r'[òóọỏõôồốộổỗơờớợởỡ]', 'o', s)
        s = re.sub(r'[ÒÓỌỎÕÔỒỐỘỔỖƠỜỚỢỞỠ]', 'O', s)
        s = re.sub(r'[ìíịỉĩ]', 'i', s)
        s = re.sub(r'[ÌÍỊỈĨ]', 'I', s)
        s = re.sub(r'[ùúụủũưừứựửữ]', 'u', s)
        s = re.sub(r'[ƯỪỨỰỬỮÙÚỤỦŨ]', 'U', s)
        s = re.sub(r'[ỳýỵỷỹ]', 'y', s)
        s = re.sub(r'[ỲÝỴỶỸ]', 'Y', s)
        s = re.sub(r'[Đ]', 'D', s)
        s = re.sub(r'[đ]', 'd', s)
        return s

    def open_spider(self, spider):
        self.client = pymongo.MongoClient("mongodb://heroku_f1mzb91l:61ra6cfnh8lse8d1ju2quaq0n9@ds239557.mlab.com:39557/heroku_f1mzb91l?retryWrites=false")
        self.db = self.client.get_default_database()
        self.comics = self.db['comics']

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        row = self.comics.count_documents({u'name': item['name']})
        if row > 0:
            print(row)
        else:
            self.comics.insert_one({
                u'name': item['name'],
                u'nameNoAccent': self.no_accent_vietnamese(item['name']),
                u'cover': item['cover'],
                u'isHot': item['isHot'],
                u'url': item['url']
            })
        
        return '-------------' + item['name']
