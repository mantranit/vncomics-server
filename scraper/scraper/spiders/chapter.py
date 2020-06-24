# -*- coding: utf-8 -*-
import scrapy
import pymongo
import time
import datetime
from scraper.items import ChapterItem

class ChapterSpider(scrapy.Spider):
    name = 'chapter'

    def start_requests(self):
        self.client = pymongo.MongoClient('mongodb+srv://vncomics:vncomics@cluster0-6ulnw.mongodb.net/vncomics?retryWrites=true&w=majority')
        self.db = self.client.vncomics
        self.comics = self.db.comics
        self.chapters = self.db.chapters
        self.row = self.chapters.find_one({"pages": {"$exists": False}})
        if self.row:
            yield scrapy.Request(url=self.row['url'], callback=self.parse)

    def parse(self, response):
        pages = response.css('#ctl00_divCenter .reading-detail .page-chapter img::attr(data-original)').getall()
        
        date_time_str = response.css('#ctl00_divCenter .reading .top i::text').extract_first()
        date_time_str = date_time_str.replace('[Cập nhật lúc: ', '')
        date_time_str = date_time_str.replace(']', '')
        tmp = datetime.datetime.strptime(date_time_str.strip(), '%H:%M %d/%m/%Y')

        comic = self.comics.find_one({"_id": self.row['comicId']})
        item_createdAt = comic['createdAt']
        if not comic['createdAt'] or comic['createdAt'] > tmp:
            item_createdAt = tmp
        item_updatedAt = comic['updatedAt']
        if not comic['updatedAt'] or comic['updatedAt'] < tmp:
            item_updatedAt = tmp
            
        self.comics.update_one({
            '_id': self.row['comicId']
        },{
            '$set': {
                'createdAt': item_createdAt,
                'updatedAt': item_updatedAt,
            }
        }, upsert=False)

        self.chapters.update_one({
            '_id': self.row['_id']
        },{
            '$set': {
                'pages': pages,
                'createdAt': tmp,
            }
        }, upsert=False)

        # next url
        time.sleep(0.5)
        self.row = self.chapters.find_one({"pages": {"$exists": False}})
        if self.row:
            yield scrapy.Request(url=self.row['url'], callback=self.parse)
        
        pass
