# -*- coding: utf-8 -*-
import scrapy
import pymongo
import datetime
from scraper.items import DetailItem

class DetailSpider(scrapy.Spider):
    name = 'detail'
    
    def start_requests(self):
        self.client = pymongo.MongoClient('mongodb+srv://vncomics:vncomics@cluster0-6ulnw.mongodb.net/vncomics?retryWrites=true&w=majority')
        self.db = self.client.vncomics
        self.comics = self.db.comics
        self.row = self.comics.find_one({"body": {"$exists": False}})

        urls = [
            self.row['url'],
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        item_body = response.css('#item-detail .detail-content p::text').extract_first()

        date_time_str = response.css('#item-detail time.small::text').extract_first()
        date_time_str = date_time_str.replace('[Cập nhật lúc: ', '')
        date_time_str = date_time_str.replace(']', '')
        updatedAt = datetime.datetime.strptime(date_time_str.strip(), '%H:%M %d/%m/%Y')

        altName = response.css('#item-detail .list-info .other-name::text').extract_first()

        self.comics.update_one({
            '_id': self.row['_id']
        },{
            '$set': {
                'body': item_body,
                'altName': altName,
                'status': 1,
                'createdAt': '',
                'updatedAt': updatedAt,
            }
        }, upsert=False)
        pass
