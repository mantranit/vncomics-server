# -*- coding: utf-8 -*-
import scrapy
import requests
import pymongo
import time
import re
from datetime import datetime
from details.items import DetailsItem

class NettruyenSpider(scrapy.Spider):
    name = 'nettruyen'
    # allowed_domains = ['nettruyen.com']
    # start_urls = ['http://nettruyen.com/']

    client = pymongo.MongoClient("mongodb+srv://vncomics:vncomics@cluster0-6ulnw.mongodb.net/vncomics?retryWrites=true&w=majority")
    db = client.vncomics
    comics = db.comics

    def get_url(self):
        while True:
            row = self.comics.find_one({"crawled": {"$exists": False}, "referer": self.name})
            if row:
                resp = requests.head(row['url'])
                if resp.status_code == 404:
                    self.comics.delete_one({"_id": row['_id']})
                else:
                    return row
            else:
                return None
        
        pass

    def start_requests(self):
        self.row = self.get_url()
        if self.row:
            yield scrapy.Request(url=self.row['url'], callback=self.parse)
        
        pass

    def parse(self, response):
        item_altName = response.css('#ctl00_divCenter .detail-info .othername .other-name::text').extract_first()
        item_body = response.css('#ctl00_divCenter .detail-content p').extract_first()
        item_body = re.sub(r'<(.*?)>', '', item_body).strip()
        item_status = response.css('#ctl00_divCenter .detail-info .status .col-xs-8::text').extract_first()
        if item_status == "Đang tiến hành":
            item_status = 0
        else:
            item_status = 1
        item_categories = response.css('#ctl00_divCenter .detail-info .kind a::text').getall()
        item_authors = response.css('#ctl00_divCenter .detail-info .author a::text').getall()
        item_chapterNames = response.css('#nt_listchapter .row .col-xs-5 a::text').getall()
        if '^# gì thế này' in item_chapterNames:
            item_chapterNames.remove('^# gì thế này')
        item_chapterUrls = response.css('#nt_listchapter .row .col-xs-5 a::attr(href)').getall()
        item_viewed = int(response.css('#ctl00_divCenter .detail-info li:last-child .col-xs-8::text').extract_first().replace('.', ''))
        item_followed = int(response.css('#ctl00_divCenter .follow b::text').extract_first().replace('.', ''))

        date_time_str = response.css('#item-detail time.small::text').extract_first()
        date_time_str = date_time_str.replace('[Cập nhật lúc: ', '')
        date_time_str = date_time_str.replace(']', '')
        item_updatedAt = datetime.strptime(date_time_str.strip(), '%H:%M %d/%m/%Y')

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
            updatedAt=item_updatedAt,
            referer=self.name
        )

        yield obj

        # next url
        time.sleep(3)
        self.row = self.get_url()
        if self.row:
            yield scrapy.Request(url=self.row['url'], callback=self.parse)
        
        pass
