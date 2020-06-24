# -*- coding: utf-8 -*-
import scrapy
import time
import datetime
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

class ChapterSpider(scrapy.Spider):
    name = 'test'

    def start_requests(self):
        cred = credentials.Certificate("D:/Mine/vncomics-server/vncomics-f3294-b440f24315e1.json")
        firebase_admin.initialize_app(cred)
        self.db = firestore.client()
        yield scrapy.Request(url="https://beeng.net/", callback=self.parse)

    def parse(self, response):
        doc_ref = self.db.collection(u'comics')
        doc_ref.document(u'test').set({
            u'first': u'Ada',
            u'last': u'Lovelace',
            u'born': 1820
        })

        query = doc_ref.where(
            u'born', u'>', 18).order_by(u'born')
        docs = query.stream()

        for doc in docs:
            print(f'{doc.id} => {doc.to_dict()}')

        pass
