# -*- coding: utf-8 -*-
import scrapy
import time
import boto3
from boto3.dynamodb.conditions import Attr
import re
from datetime import datetime
from chapters.items import ChaptersItem

class NettruyenSpider(scrapy.Spider):
    name = 'nettruyen'
    # allowed_domains = ['nettruyen.com']
    # start_urls = ['http://nettruyen.com/']

    dynamodb = boto3.resource('dynamodb')
    chapters = dynamodb.Table('chapters')

    segment = 1283

    def get_url(self):
        while True:
            docs = self.chapters.scan(
                FilterExpression=Attr('crawled').eq(False) & Attr('referer').eq(self.name),
                Segment=self.segment,
                TotalSegments=20001
            )
            if docs['Count'] > 0:
                return docs['Items'][0]
            elif self.segment < 20000:
                self.segment = self.segment + 1
            else:
                return None
        
        return None

        pass

    def start_requests(self):
        self.item = self.get_url()
        if self.item:
            url = self.item['url']
            url = url.replace("my-dear-cold-blooded-king", "huyet-de-bao-chua")
            url = url.replace("man-up-girl", "cung-len-nao-chang-trai")
            print('----------'+str(self.segment)+'-----------' + url + '----------------')
            yield scrapy.Request(url=url, callback=self.parse)
        pass

    def parse(self, response):
        date_time_str = response.css('#ctl00_divCenter .top i::text').extract_first()
        date_time_str = date_time_str.replace('[Cập nhật lúc: ', '')
        date_time_str = date_time_str.replace(']', '')
        item_createdAt = datetime.strptime(date_time_str.strip(), '%H:%M %d/%m/%Y')
        
        item_pages = response.css('#ctl00_divCenter .reading-detail .page-chapter img::attr(data-original)').getall()

        obj = ChaptersItem(
            id=self.item['id'],
            comicId=self.item['comicId'],
            pages=item_pages,
            createdAt=item_createdAt
        )

        yield obj
        
        time.sleep(1)
        self.item = self.get_url()
        if self.item:
            url = self.item['url']
            url = url.replace("my-dear-cold-blooded-king", "huyet-de-bao-chua")
            url = url.replace("man-up-girl", "cung-len-nao-chang-trai")
            print('----------'+str(self.segment)+'-----------' + url + '----------------')
            yield scrapy.Request(url=url, callback=self.parse)
        
        pass
