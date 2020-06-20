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

        # DATABASE_URL = os.environ['DATABASE_URL']
        self.connection = psycopg2.connect('postgres://pefchungjyxqgi:ee9a6f4ebd93f8b97ac67e4c1a34d910e73b77cc866fe40bab5b5587cc79aedb@ec2-52-87-135-240.compute-1.amazonaws.com:5432/ddu8s5pp7ddfbi', sslmode='require')
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
