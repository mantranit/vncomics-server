# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import os
import psycopg2

class ComicPipeline(object):

    def open_spider(self, spider):
        # hostname = 'localhost'
        # username = 'postgres'
        # password = '12345'
        # database = 'vncomics'
        # self.connection = psycopg2.connect(host=hostname, user=username, password=password, dbname=database)

        DATABASE_URL = os.environ['DATABASE_URL']
        self.connection = psycopg2.connect(DATABASE_URL, sslmode='require')
        self.cur = self.connection.cursor()

    def close_spider(self, spider):
        self.cur.close()
        self.connection.close()

    def process_item(self, item, spider):
        self.cur.execute("SELECT count(*) as total FROM comics WHERE name = %(name)s", { 'name': item['name'] })
        row = self.cur.fetchone()[0]
        if row == 0:
            self.cur.execute("INSERT INTO comics(name,cover,url) VALUES(%s,%s,%s)", (item['name'],item['cover'],item['url']))
        else:
            print("Already exists")
        self.connection.commit()
        return item
