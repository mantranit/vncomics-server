# -*- coding: utf-8 -*-
import scrapy
import time
import requests
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

    logFile = open("crawled.log","a+")
    segment = 10915

    def get_url(self):
        while True:
            docs = self.chapters.scan(
                FilterExpression=Attr('crawled').eq(False) & Attr('referer').eq(self.name),
                Segment=self.segment,
                TotalSegments=20001
            )
            if docs['Count'] > 0:
                item = docs['Items'][0]
                resp = requests.head(item['url'])
                if resp.status_code == 404:
                    lines = self.logFile.readlines()
                    lines.append("ERROR: " + item['url'] + "\n")
                    self.logFile.writelines(lines)

                    self.chapters.delete_item(
                        Key = {
                            "id": item['id']
                        }
                    )

                # if resp.status_code == 301:
                #     lines = self.logFile.readlines()
                #     lines.append("WARN: " + item['url'] + "\n")
                #     self.logFile.writelines(lines)

                #     self.chapters.delete_item(
                #         Key = {
                #             "id": item['id']
                #         }
                #     )
                    
                else:
                    return item
            elif self.segment < 20000:
                self.segment = self.segment + 1
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
        
        self.item = self.get_url()
        if self.item:
            print('----------'+str(self.segment)+'-----------' + self.item['url'] + '----------------')
            time.sleep(1)
            yield scrapy.Request(url=self.item['url'], callback=self.parse)
        
        pass
