# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import os
import pymongo

class ComicPipeline(object):

    def open_spider(self, spider):
        self.client = pymongo.MongoClient('mongodb+srv://vncomics:vncomics@cluster0-6ulnw.mongodb.net/vncomics?retryWrites=true&w=majority')
        self.db = self.client.vncomics

    # def close_spider(self, spider):
    #     self.cur.close()
    #     self.connection.close()

    def process_item(self, item, spider):
        comics = self.db.comics
        row = comics.find({'name': item['name']}).count()
        if row > 0:
            print("Already exists")
        else:
            comics.insert_one({'name': item['name'], 'cover': item['cover'], 'url': item['url']})
        return item


class DetailPipeline(object):

    def open_spider(self, spider):
        self.client = pymongo.MongoClient('mongodb+srv://vncomics:vncomics@cluster0-6ulnw.mongodb.net/vncomics?retryWrites=true&w=majority')
        self.db = self.client.vncomics

    # def close_spider(self, spider):
    #     self.cur.close()
    #     self.connection.close()

    def process_item(self, item, spider):
        # comics = self.db.comics
        # row = comics.find({'name': item['name']}).count()
        # if row > 0:
        #     print("Already exists")
        # else:
        #     comics.insert_one({'name': item['name'], 'cover': item['cover'], 'url': item['url']})
        print(item)
        return item
