# -*- coding: utf-8 -*-
import scrapy
import time
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

class NettruyenSpider(scrapy.Spider):
    name = 'nettruyen'
    # allowed_domains = ['nettruyen.com']
    # start_urls = ['http://nettruyen.com/']

    def start_requests(self):
        cred = credentials.Certificate("D:/Mine/vncomics-server/vncomics-firebase-adminsdk-nkc27-5cc4733250.json")
        firebase_admin.initialize_app(cred)
        self.db = firestore.client()
        self.chapters = self.db.collection(u'chapters')

        print('-------------------------1-----------------------')
        docs = self.chapters.limit(1).stream()
        # for doc in docs:
        #     print(f'{doc.id} => {doc.to_dict()}')
        rows = list(docs)
        if len(rows) > 0:
            data = rows[0].to_dict()
        print(docs)
        print('-------------------------2-----------------------')
        print(rows[0].to_dict())
        print('-------------------------3-----------------------')

        # yield scrapy.Request(url="http://www.nettruyen.com/", callback=self.parse)
        pass

    def parse(self, response):
        item_createdAt = response.css('#ctl00_divCenter .top i::text').extract_first()
        item_pages = response.css('#ctl00_divCenter .reading-detail .page-chapter img::attr(data-original)').getall()

        yield({
            u'comicId': item_pages,
            u'pages': item_pages,
            u'createdAt': item_createdAt
        })
        
        time.sleep(2)
        next_url_path = response.css(".pagination a.next-page::attr('href')").extract_first()
        if next_url_path:
            yield scrapy.Request(url=next_url_path, callback=self.parse)
        
        pass
