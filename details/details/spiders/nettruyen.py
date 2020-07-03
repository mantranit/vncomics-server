# -*- coding: utf-8 -*-
import scrapy
import requests
import pymongo
import time
from datetime import datetime

class NettruyenSpider(scrapy.Spider):
    name = 'nettruyen'
    # allowed_domains = ['nettruyen.com']
    # start_urls = ['http://nettruyen.com/']

    def start_requests(self):
        self.client = pymongo.MongoClient("mongodb://heroku_f1mzb91l:61ra6cfnh8lse8d1ju2quaq0n9@ds239557.mlab.com:39557/heroku_f1mzb91l?retryWrites=false")
        self.db = self.client.get_default_database()
        self.comics = self.db['comics']
        
        self.row = self.comics.find_one({"crawled": {"$exists": False}})
        if self.row:
            resp = requests.head(self.row['url'])
            if resp.status_code == 404:
                self.comics.delete_one({"_id": self.row['_id']})
            else:
                yield scrapy.Request(url=self.row['url'], callback=self.parse)

    def parse(self, response):
        item_altName = response.css('#ctl00_divCenter .detail-info .othername .other-name::text').extract_first()
        item_body = response.css('#ctl00_divCenter .detail-content p::text').extract_first()
        item_status = response.css('#ctl00_divCenter .detail-info .status .col-xs-8::text').extract_first()
        if item_status == "Đang tiến hành":
            item_status = 0
        else:
            item_status = 1
        item_categories = response.css('#ctl00_divCenter .detail-info .kind a::text').getall()
        item_authors = response.css('#ctl00_divCenter .detail-info .author a::text').getall()
        item_chapters_name = response.css('#nt_listchapter .row .col-xs-5 a::text').getall()
        item_chapters_url = response.css('#nt_listchapter .row .col-xs-5 a::attr(href)').getall()
        item_viewed = int(response.css('#ctl00_divCenter .detail-info li:last-child .col-xs-8::text').extract_first().replace('.', ''))
        item_followed = int(response.css('#ctl00_divCenter .follow b::text').extract_first().replace('.', ''))

        date_time_str = response.css('#item-detail time.small::text').extract_first()
        date_time_str = date_time_str.replace('[Cập nhật lúc: ', '')
        date_time_str = date_time_str.replace(']', '')
        item_updatedAt = datetime.strptime(date_time_str.strip(), '%H:%M %d/%m/%Y')

        yield({
            u'comicId': self.row['_id'],
            u'name': self.row['name'],
            u'altName': item_altName,
            u'body': item_body,
            u'status': item_status,
            u'categories': item_categories,
            u'authors': item_authors,
            u'chapters': {
                u'name': item_chapters_name,
                u'url': item_chapters_url,
            },
            u'viewed': item_viewed,
            u'followed': item_followed,
            u'updatedAt': item_updatedAt
        })

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
