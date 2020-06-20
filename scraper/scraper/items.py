# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

class ComicItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field()
    cover = scrapy.Field()
    url = scrapy.Field()

class DetailItem(scrapy.Item):
    # define the fields for your item here like:
    body = scrapy.Field()
