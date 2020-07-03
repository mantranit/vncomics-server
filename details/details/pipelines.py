# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo
import re
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from uuid import uuid4

class DetailsPipeline:
    
    def open_spider(self, spider):
        self.client = pymongo.MongoClient("mongodb://heroku_f1mzb91l:61ra6cfnh8lse8d1ju2quaq0n9@ds239557.mlab.com:39557/heroku_f1mzb91l?retryWrites=false")
        self.db = self.client.get_default_database()
        self.comics = self.db['comics']
        self.categories = self.db['categories']
        self.authors = self.db['authors']

        cred = credentials.Certificate("D:/Mine/vncomics-server/vncomics-firebase-adminsdk-nkc27-5cc4733250.json")
        firebase_admin.initialize_app(cred)
        self.db = firestore.client()
        self.chapters = self.db.collection(u'chapters')

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):

        item_cat = []
        categories = item['categories']
        for i in (range(len(categories))):
            cat_id = ''
            row = self.categories.find_one({"name": categories[i]})
            if not row:
                row = self.categories.insert_one({
                    "name": categories[i]
                })
                cat_id = row.inserted_id
            else:
                cat_id = row['_id']
            item_cat.append(cat_id)

        item_aut = []
        authors = item['authors']
        for i in (range(len(authors))):
            cat_id = ''
            row = self.authors.find_one({"name": authors[i]})
            if not row:
                row = self.authors.insert_one({
                    "name": authors[i]
                })
                cat_id = row.inserted_id
            else:
                cat_id = row['_id']
            item_aut.append(cat_id)

        item_cha = []
        chapters = item['chapters']
        for i in (range(len(chapters['name']))):
            cha_id = str(uuid4())

            docs = self.chapters.where(u'comicId', u'==', str(item['comicId'])).where(u'name', u'==', chapters['name'][i]).stream()
            rows = list(docs)
            if len(rows) == 0:
                self.chapters.document(cha_id).set({
                    u'comicId': str(item['comicId']),
                    u'comicName': item['name'],
                    u'name': chapters['name'][i],
                    u'url': chapters['url'][i],
                    u'pages': [],
                    u'crawled': False
                })
            else:
                cha_id = rows[0].id
            item_cha.append({ 'name': chapters['name'][i], 'chapterId': cha_id })
        
        self.comics.update_one({
            '_id': item['comicId']
        },{
            '$set': {
                u'altName': item['altName'],
                u'body': item['body'],
                u'status': item['status'],
                u'categories': item_cat,
                u'authors': item_aut,
                u'chapters': item_cha,
                u'viewed': item['viewed'],
                u'followed': item['followed'],
                u'createdAt': item['updatedAt'],
                u'updatedAt': item['updatedAt']
            }
        }, upsert=False)

        # return item['name']
