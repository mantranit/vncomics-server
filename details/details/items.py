# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class DetailsItem(scrapy.Item):
    # define the fields for your item here like:
    comicId = scrapy.Field()
    name = scrapy.Field()
    altName = scrapy.Field()
    body = scrapy.Field()
    status = scrapy.Field()
    categories = scrapy.Field()
    authors = scrapy.Field()
    chapters = scrapy.Field()
    viewed = scrapy.Field()
    followed = scrapy.Field()
    updatedAt = scrapy.Field()
    pass
