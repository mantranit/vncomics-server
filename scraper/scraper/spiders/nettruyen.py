# -*- coding: utf-8 -*-
import scrapy
import time
from scraper.items import ComicItem

class NettruyenSpider(scrapy.Spider):
    name = 'nettruyen'
    allowed_domains = ['nettruyen.com']
    start_urls = ['http://nettruyen.com/']

    # def start_requests(self):
    #     urls = [
    #         'http://www.nettruyen.com/',
    #     ]
    #     for url in urls:
    #         yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        for block in response.css('#ctl00_divCenter .item'):
            item_name = block.css('h3 a::text').extract_first()
            item_cover = block.css('.image img::attr(data-original)').extract_first()
            item_url = block.css('h3 a::attr(href)').extract_first()
            obj = ComicItem(name=item_name,cover=item_cover,url=item_url)
            yield obj

        time.sleep(2)
        next_url_path = response.css("#ctl00_divCenter .pagination a.next-page::attr('href')").extract_first()
        if next_url_path:
            yield scrapy.Request(
                url=next_url_path,
                callback=self.parse
            )
