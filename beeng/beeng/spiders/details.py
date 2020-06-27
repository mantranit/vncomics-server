# -*- coding: utf-8 -*-
import scrapy
import pymongo
import time
import datetime
import requests
import re

class DetailsSpider(scrapy.Spider):
    name = 'details'
    allowed_domains = ['beeng.net']

    def start_requests(self):
        self.client = pymongo.MongoClient('mongodb+srv://vncomics:vncomics@cluster0-6ulnw.mongodb.net/vncomics?retryWrites=true&w=majority')
        self.db = self.client.vncomics
        self.comics = self.db.comics
        self.category = self.db.categories
        self.authors = self.db.authors
        self.chapters = self.db.chapters
        self.row = self.comics.find_one({"crawled": {"$exists": False}})
        if self.row:
            resp = requests.head(self.row['url'])
            if resp.status_code == 404:
                self.comics.delete_one({"_id": self.row['_id']})
            else:
                yield scrapy.Request(url=self.row['url'], callback=self.parse)

    def parse(self, response):
        item_body = response.css('.manga-info-main .manga-summary::text').extract_first().strip()

        item_altName = response.css('.manga-info-main .manga-detail li:nth-child(5)').extract_first()
        item_altName = re.sub(r'<span(.*?)span>', '', item_altName)
        item_altName = re.sub(r'<(.*?)>', '', item_altName).strip()
        if item_altName == "Đang cập nhật":
            item_altName = ""

        status = response.css('.manga-info-main .manga-detail li:nth-child(9)').extract_first()
        status = re.sub(r'<span(.*?)span>', '', status)
        status = re.sub(r'<(.*?)>', '', status).strip()
        item_status = 0
        if status == "Đã hoàn thành":
            item_status = 1

        hrefs = response.css('.manga-info-main .manga-detail li:nth-child(7) a::attr(href)').getall()
        names = response.css('.manga-info-main .manga-detail li:nth-child(7) a::text').getall()
        item_cat = []
        for i in reversed(range(len(names))):
            cat_id = ''
            row = self.category.find_one({"name": names[i]})
            if not row:
                row = self.category.insert_one({"name": names[i], "url": 'https://beeng.net' + hrefs[i]})
                cat_id = row.inserted_id
            else:
                cat_id = row['_id']
            
            item_cat.append(cat_id)

        names = response.css('.manga-info-main .manga-detail li:nth-child(4) span:not(.font-bold)::text').getall()
        item_aut = []
        for i in reversed(range(len(names))):
            if names[i] != "Đang cập nhật":
                aut_id = ''
                row = self.authors.find_one({"name": names[i]})
                if not row:
                    row = self.authors.insert_one({"name": names[i]})
                    aut_id = row.inserted_id
                else:
                    aut_id = row['_id']
                
                item_aut.append(aut_id)

        item_createdAt = ''
        item_updatedAt = ''

        item_cha = []
        for block in reversed(response.css('.manga-info-main .manga-chapter .u84ho3')):
            cha_name = block.css('a::text').extract_first()
            cha_url = 'https://beeng.net' + block.css('a::attr(href)').extract_first()

            date_time_str = block.css('.date::text').extract_first()
            cha_createdAt = datetime.datetime.strptime(date_time_str.strip(), '%d/%m/%Y')

            if cha_name:
                cha_id = ''
                row = self.chapters.find_one({"comicId": self.row['_id'], "name": cha_name})
                if not row:
                    row = self.chapters.insert_one({"comicId": self.row['_id'], "name": cha_name, "url": cha_url, "createdAt": cha_createdAt})
                    cha_id = row.inserted_id
                else:
                    cha_id = row['_id']
                
                item_cha.append(cha_id)

                # update createdAt and updatedAt
                if not item_createdAt or item_createdAt > cha_createdAt:
                    item_createdAt = cha_createdAt
                if not item_updatedAt or item_updatedAt < cha_createdAt:
                    item_updatedAt = cha_createdAt

        self.comics.update_one({
            '_id': self.row['_id']
        },{
            '$set': {
                'altName': item_altName,
                'body': item_body,
                'status': item_status,
                'categories': item_cat,
                'authors': item_aut,
                'chapters': item_cha,
                'createdAt': item_createdAt,
                'updatedAt': item_updatedAt,
                'crawled': True
            }
        }, upsert=False)

        # next url
        time.sleep(0.2)
        self.row = self.comics.find_one({"crawled": {"$exists": False}})
        if self.row:
            resp = requests.head(self.row['url'])
            if resp.status_code == 404:
                self.comics.delete_one({"_id": self.row['_id']})
            else:
                yield scrapy.Request(url=self.row['url'], callback=self.parse)
        
        pass
