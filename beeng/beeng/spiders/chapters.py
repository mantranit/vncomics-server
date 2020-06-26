# -*- coding: utf-8 -*-
import scrapy
import pymongo
import time

class ChaptersSpider(scrapy.Spider):
    name = 'chapters'
    allowed_domains = ['beeng.net']
    # start_urls = ['http://beeng.net/']

    def start_requests(self):
        self.client = pymongo.MongoClient('mongodb+srv://vncomics:vncomics@cluster0-6ulnw.mongodb.net/vncomics?retryWrites=true&w=majority')
        self.db = self.client.vncomics
        self.chapters = self.db.chapters
        self.row = self.chapters.find_one({"pages": {"$exists": False}})
        if self.row:
            yield scrapy.Request(url=self.row['url'], callback=self.parse)

    def parse(self, response):

        list = response.css("#image-load a img::attr(src)").getall()
        self.chapters.update_one({
            '_id': self.row['_id']
        },{
            '$set': {
                'pages': list,
            }
        }, upsert=False)

        time.sleep(2)
        self.row = self.chapters.find_one({"pages": {"$exists": False}})
        if self.row:
            yield scrapy.Request(url=self.row['url'], callback=self.parse)

        pass
