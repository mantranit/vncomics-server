# -*- coding: utf-8 -*-
import scrapy
import time
from datetime import datetime
from uuid import uuid4
from urllib.parse import unquote_plus

class NettruyenSpider(scrapy.Spider):
    name = 'nettruyen'
    # allowed_domains = ['nettruyen.com']
    # start_urls = ['http://nettruyen.com/']

    def start_requests(self):
        yield scrapy.Request(url="http://www.nettruyen.com/", callback=self.parse)
        pass

    def parse(self, response):
        for block in response.css('#ctl00_divCenter .items .item'):
            item_name = block.css('h3 a::text').extract_first()
            item_cover = block.css('.image img::attr(data-original)').extract_first()
            item_cover = unquote_plus(item_cover)
            item_url = block.css('h3 a::attr(href)').extract_first()

            yield({
                u'name': item_name,
                u'cover': item_cover,
                u'url': item_url
            })

        time.sleep(2)
        next_url_path = response.css(".pagination a.next-page::attr('href')").extract_first()
        if next_url_path:
            yield scrapy.Request(url=next_url_path, callback=self.parse)
        
        pass
