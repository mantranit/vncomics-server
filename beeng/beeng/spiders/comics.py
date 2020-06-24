# -*- coding: utf-8 -*-
import scrapy
import time
import uuid
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

class ComicsSpider(scrapy.Spider):
    name = 'comics'
    allowed_domains = ['beeng.net']
    # start_urls = ['https://beeng.net/']

    def start_requests(self):
        cred = credentials.Certificate("D:/Mine/vncomics-server/vncomics-f3294-b440f24315e1.json")
        firebase_admin.initialize_app(cred)
        self.db = firestore.client()
        self.comics = self.db.collection(u'comics')

        yield scrapy.Request(url="https://beeng.net/the-loai", callback=self.parse)

    def parse(self, response):
        batch = self.db.batch()

        for block in response.css('.genre-main .manga-list .item'):
            item_name = block.css('.row .info .tit a::text').extract_first()
            item_cover = block.css('.row .img img::attr(src)').extract_first()
            item_url = 'https://beeng.net' + block.css('.row .img::attr(href)').extract_first()

            docs = self.db.collection(u'comics').where(u'name', u'==', item_name).stream()
            if not len(list(docs)):
                batch.set(self.comics.document(str(uuid.uuid4())), {
                    u'name': item_name,
                    u'cover': item_cover,
                    u'url': item_url
                })

        batch.commit()

        # docs = self.db.collection(u'comics').stream()
        # i = 0
        # for doc in docs:
        #     i+=1
        # print('---------------------------------------------------------------------------------')
        # print(i)
        # print('---------------------------------------------------------------------------------')

        time.sleep(2)
        next_url_path = response.css(".genre-main .pagination li:last-child a::attr('href')").extract_first()
        if next_url_path:
            yield scrapy.Request(url=next_url_path, callback=self.parse)
        pass
