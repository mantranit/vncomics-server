# -*- coding: utf-8 -*-
import scrapy
import time
import pymongo

class ComicsSpider(scrapy.Spider):
    name = 'comics'
    allowed_domains = ['beeng.net']

    def start_requests(self):
        yield scrapy.Request(url="https://beeng.net/the-loai", callback=self.parse)

    def parse(self, response):

        for block in response.css('.genre-main .manga-list .item'):
            item_name = block.css('.row .info .tit a::text').extract_first().encode('utf-8')
            item_cover = block.css('.row .img img::attr(src)').extract_first()
            item_cover = item_cover.replace("https://beeng.net/cover/80x110/", "")
            item_url = 'https://beeng.net' + block.css('.row .img::attr(href)').extract_first()

            yield({
                u'name': item_name,
                u'cover': item_cover,
                u'url': item_url
            })

        time.sleep(2)
        # next_url_path = response.css(".genre-main .pagination li:last-child a::attr('href')").extract_first()
        # if next_url_path and next_url_path != "#":
        #     yield scrapy.Request(url=next_url_path, callback=self.parse)
        # else:
        #     self.client.close()
        
        pass
