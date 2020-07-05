# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import pymongo
import os
import re

class ComicsPipeline:

    def no_accent_vietnamese(self, s):
        s = re.sub(r'[àáạảãâầấậẩẫăằắặẳẵ]', 'a', s)
        s = re.sub(r'[ÀÁẠẢÃĂẰẮẶẲẴÂẦẤẬẨẪ]', 'A', s)
        s = re.sub(r'[èéẹẻẽêềếệểễ]', 'e', s)
        s = re.sub(r'[ÈÉẸẺẼÊỀẾỆỂỄ]', 'E', s)
        s = re.sub(r'[òóọỏõôồốộổỗơờớợởỡ]', 'o', s)
        s = re.sub(r'[ÒÓỌỎÕÔỒỐỘỔỖƠỜỚỢỞỠ]', 'O', s)
        s = re.sub(r'[ìíịỉĩ]', 'i', s)
        s = re.sub(r'[ÌÍỊỈĨ]', 'I', s)
        s = re.sub(r'[ùúụủũưừứựửữ]', 'u', s)
        s = re.sub(r'[ƯỪỨỰỬỮÙÚỤỦŨ]', 'U', s)
        s = re.sub(r'[ỳýỵỷỹ]', 'y', s)
        s = re.sub(r'[ỲÝỴỶỸ]', 'Y', s)
        s = re.sub(r'[Đ]', 'D', s)
        s = re.sub(r'[đ]', 'd', s)
        return s

    def open_spider(self, spider):
        self.client = pymongo.MongoClient("mongodb+srv://vncomics:vncomics@cluster0-6ulnw.mongodb.net/vncomics?retryWrites=true&w=majority")
        self.db = self.client.vncomics
        self.comics = self.db.comics
        self.categories = self.db.categories
        self.authors = self.db.authors

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):

        rowComic = self.comics.find_one({u'name': item['name']})

        if "nonexistent altName" in item:
            if rowComic == 0:
                self.comics.insert_one({
                    u'name': item['name'],
                    u'nameNoAccent': self.no_accent_vietnamese(item['name']),
                    u'cover': item['cover'],
                    u'isHot': item['isHot'],
                    u'url': item['url']
                })
        else:
            if rowComic > 0:
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
                
                self.comics.update_one({
                    '_id': rowComic['_id']
                },{
                    '$set': {
                        u'cover': item['cover'],
                        u'altName': item['altName'],
                        u'body': item['body'],
                        u'status': item['status'],
                        u'categories': item_cat,
                        u'authors': item_aut,
                        u'viewed': item['viewed'],
                        u'followed': item['followed'],
                        u'createdAt': item['updatedAt'],
                        u'updatedAt': item['updatedAt']
                    }
                }, upsert=False)
        
        return item
