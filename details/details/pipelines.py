# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo
import re
import boto3
from boto3.dynamodb.conditions import Attr
from uuid import uuid4

class DetailsPipeline:
    
    def open_spider(self, spider):
        self.client = pymongo.MongoClient("mongodb+srv://vncomics:vncomics@cluster0-6ulnw.mongodb.net/vncomics?retryWrites=true&w=majority")
        self.db = self.client.vncomics
        self.comics = self.db.comics
        self.categories = self.db.categories
        self.authors = self.db.authors

        dynamodb = boto3.resource('dynamodb')
        self.chapters = dynamodb.Table('chapters')

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
            if authors[i] != "Đang Cập Nhật":
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
        chapterNames = item['chapterNames']
        chapterUrls = item['chapterUrls']
        for i in (range(len(chapterNames))):
            cha_id = str(uuid4())

            docs = self.chapters.scan(FilterExpression=Attr('comicId').eq(str(item['comicId'])) & Attr('name').eq(chapterNames[i]))
            
            if docs['Count'] == 0:
                self.chapters.put_item(
                    Item = {
                        u'id': cha_id,
                        u'comicId': str(item['comicId']),
                        u'comicName': item['name'],
                        u'name': chapterNames[i],
                        u'url': chapterUrls[i],
                        u'pages': False,
                        u'referer': item['referer']
                    }
                )
            else:
                cha_id = docs['Items'][0]['id']
            item_cha.append({ 'name': chapterNames[i], 'chapterId': cha_id })
        
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

        return '---------------------------------------------'
