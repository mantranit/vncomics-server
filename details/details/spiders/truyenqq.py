# -*- coding: utf-8 -*-
import scrapy
import requests
import pymongo
import time
import re
from datetime import datetime
from details.items import DetailsItem

class TruyenqqSpider(scrapy.Spider):
    name = 'truyenqq'
    # allowed_domains = ['truyenqq.com']
    # start_urls = ['http://truyenqq.com/']

    client = pymongo.MongoClient("mongodb+srv://vncomics:vncomics@cluster0-6ulnw.mongodb.net/vncomics?retryWrites=true&w=majority")
    db = client.vncomics
    comics = db.comics

    def get_url(self):
        while True:
            row = self.comics.find_one({"body": {"$exists": False}})
            if row:
                resp = requests.head(row['url'])
                if resp.status_code == 404:
                    self.comics.delete_one({"_id": row['_id']})
                else:
                    return row
            else:
                return None

    def start_requests(self):
        self.row = self.get_url()
        if self.row:
            yield scrapy.Request(url=self.row['url'], callback=self.parse)

    def parse(self, response):
        item_altName = None
        item_body = response.css('.main-content .center .story-detail-info').extract_first()
        item_body = re.sub(r'<(.*?)>', '', item_body).strip()
        item_status = response.css('.main-content .center .txt .info-item:nth-child(2)::text').extract_first()
        if item_status == "Tình trạng: Đang Cập Nhật":
            item_status = 0
        else:
            item_status = 1
        item_categories = response.css('.main-content .center .list01 li a::text').getall()
        item_authors = response.css('.main-content .center .txt .info-item:nth-child(1) a::text').getall()
        item_chapterNames = response.css('.main-content .works-chapter-list .row a::text').getall()
        item_chapterUrls = response.css('.main-content .works-chapter-list .row a::attr(href)').getall()

        for sp01 in response.css('.main-content .center .txt div .sp01'):
            if sp01.css('.fa-heart'):
                item_followed = int(sp01.css('.sp02::text').extract_first().replace(',', ''))
            if sp01.css('.fa-eye'):
                item_viewed = int(sp01.css('.sp02::text').extract_first().replace(',', ''))
        item_updatedAt = None

        obj = DetailsItem(
            comicId=self.row['_id'],
            name=self.row['name'],
            altName=item_altName,
            body=item_body,
            status=item_status,
            categories=item_categories,
            authors=item_authors,
            chapterNames=item_chapterNames,
            chapterUrls=item_chapterUrls,
            viewed=item_viewed,
            followed=item_followed,
            updatedAt=item_updatedAt
        )

        yield obj

        # next url
        time.sleep(1)
        next_url = self.get_url()
        if next_url:
            yield scrapy.Request(url=next_url, callback=self.parse)
        
        pass
