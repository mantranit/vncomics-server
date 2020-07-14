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

    segment = 18822

    def get_url(self):
        while True:
            docs = self.chapters.scan(
                FilterExpression=Attr('crawled').eq(False) & Attr('referer').eq(self.name) & Attr('comicId').ne('5f040a8656fb09dfd5cbafbe') & Attr('comicId').ne('5f0411ec56fb09dfd5cbbcd3') & Attr('comicId').ne('5f040c7456fb09dfd5cbb2cc'),
                Segment=self.segment,
                TotalSegments=20001
            )
            if docs['Count'] > 0:
                item = docs['Items'][0]
                url = item['url']
                url = url.replace("my-dear-cold-blooded-king", "huyet-de-bao-chua")
                url = url.replace("man-up-girl", "cung-len-nao-chang-trai")
                url = url.replace("medical-return", "bac-si-trung-sinh")
                url = url.replace("gleipnir", "soi-xich-than")
                url = url.replace("nettruyen.com/truyen-tranh/dia-nguc-cuc-lac", "nhattruyen.com/truyen-tranh/dia-nguc-cuc-lac")
                url = url.replace("ouroboros", "cong-ly-va-bong-toi")
                url = url.replace("so-tay-nuoi-dung-than-tuong-len-duong-thoi", "so-tay-nuoi-duong-than-tuong-len-duong-thoi")
                url = url.replace("shiyakusho", "van-phong-cong-chung-sau-khi-chet")

                item['url'] = url
                return item
            elif self.segment > 0:
                self.segment = self.segment - 1
            else:
                return None
        
        return None

        pass

    def start_requests(self):
        self.item = self.get_url()
        if self.item:
            print('----------'+str(self.segment)+'-----------' + self.item['url'] + '----------------')
            yield scrapy.Request(url=self.item['url'], callback=self.parse)
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
            print('----------'+str(self.segment)+'-----------' + self.item['url'] + '----------------')
            yield scrapy.Request(url=self.item['url'], callback=self.parse)
        
        pass
