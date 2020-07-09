# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo
import boto3
from datetime import datetime
from bson import ObjectId

class ChaptersPipeline:
    def open_spider(self, spider):
        self.client = pymongo.MongoClient("mongodb+srv://vncomics:vncomics@cluster0-6ulnw.mongodb.net/vncomics?retryWrites=true&w=majority")
        self.db = self.client.vncomics
        self.comics = self.db.comics

        dynamodb = boto3.resource('dynamodb')
        self.chapters = dynamodb.Table('chapters')

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):

        response = self.chapters.update_item(
            Key={
                'id': item['id']
            },
            UpdateExpression="set pages=:p, createdAt=:c, crawled=:cr",
            ExpressionAttributeValues={
                ':p': item['pages'],
                ':c': item['createdAt'].strftime("%Y-%m-%d %H:%M:%S"),
                ':cr': True
            },
            ReturnValues="UPDATED_NEW"
        )

        rowComic = self.comics.find_one({ "_id": ObjectId(item['comicId']) })

        item_createdAt = rowComic['createdAt']
        if item_createdAt > item['createdAt']:
            item_createdAt = item['createdAt']
        item_updatedAt = rowComic['updatedAt']
        if item_updatedAt < item['createdAt']:
            item_updatedAt = item['createdAt']

        self.comics.update_one({
            '_id': rowComic['_id']
        },{
            '$set': {
                u'createdAt': item_createdAt,
                u'updatedAt': item_updatedAt
            }
        }, upsert=False)

        return '-----------'+item['comicId']+'--------------'+item['id']+'-------------'
        pass
