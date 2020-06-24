# -*- coding: utf-8 -*-
import scrapy
import pymongo
import time
import datetime
from scraper.items import DetailItem

class DetailSpider(scrapy.Spider):
    name = 'chapter'
    
    def start_requests(self):
        self.client = pymongo.MongoClient('mongodb+srv://vncomics:vncomics@cluster0-6ulnw.mongodb.net/vncomics?retryWrites=true&w=majority')
        self.db = self.client.vncomics
        self.comics = self.db.comics
        self.category = self.db.categories
        self.authors = self.db.authors
        self.row = self.comics.find_one({"chapters": {"$exists": False}})
        if self.row:
            yield scrapy.Request(url=self.row['url'], callback=self.parse)

    def parse(self, response):

        item_body = response.css('#item-detail .detail-content p::text').extract_first()

        date_time_str = response.css('#item-detail time.small::text').extract_first()
        date_time_str = date_time_str.replace('[Cập nhật lúc: ', '')
        date_time_str = date_time_str.replace(']', '')
        item_updatedAt = datetime.datetime.strptime(date_time_str.strip(), '%H:%M %d/%m/%Y')

        item_altName = response.css('#item-detail .list-info .other-name::text').extract_first()
        status = response.css('#item-detail .list-info .status .col-xs-8::text').extract_first()
        item_status = 0
        if status == 'Hoàn thành':
            item_status = 1

        hrefs = response.css('#item-detail .list-info .kind a::attr(href)').getall()
        names = response.css('#item-detail .list-info .kind a::text').getall()
        item_cat = []
        for i in range(len(names)):
            cat_id = ''
            row = self.category.find_one({"name": names[i]})
            if not row:
                row = self.category.insert_one({"name": names[i], "url": hrefs[i]})
                cat_id = row.inserted_id
            else:
                cat_id = row['_id']
            
            item_cat.append(cat_id)

        hrefs = response.css('#item-detail .list-info .author a::attr(href)').getall()
        names = response.css('#item-detail .list-info .author a::text').getall()
        item_aut = []
        for i in range(len(names)):
            aut_id = ''
            row = self.authors.find_one({"name": names[i]})
            if not row:
                row = self.authors.insert_one({"name": names[i], "url": hrefs[i]})
                aut_id = row.inserted_id
            else:
                aut_id = row['_id']
            
            item_aut.append(aut_id)

        self.comics.update_one({
            '_id': self.row['_id']
        },{
            '$set': {
                'altName': item_altName,
                'body': item_body,
                'status': item_status,
                'categories': item_cat,
                'authors': item_aut,
                'createdAt': '',
                'updatedAt': item_updatedAt,
            }
        }, upsert=False)

        # next url
        # time.sleep(0.2)
        self.row = self.comics.find_one({"chapters": {"$exists": False}})
        if self.row:
            yield scrapy.Request(url=self.row['url'], callback=self.parse)
        
        pass
