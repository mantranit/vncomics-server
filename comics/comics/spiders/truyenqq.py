# -*- coding: utf-8 -*-
import scrapy
import time
from urllib.parse import unquote_plus
from comics.items import ComicsItem

class TruyenqqSpider(scrapy.Spider):
    name = 'truyenqq'
    # allowed_domains = ['truyenqq.com']
    # start_urls = ['http://truyenqq.com/']

    def start_requests(self):
        yield scrapy.Request(url="http://truyenqq.com/truyen-moi-cap-nhat/trang-1.html", callback=self.parse)
        pass

    def parse(self, response):
        for block in response.css('.main-content .list-stories li'):
            item_name = block.css('.story-item > a::attr(title)').extract_first()
            item_cover = block.css('.story-item > a img::attr(src)').extract_first()
            item_cover = unquote_plus(item_cover)
            item_url = block.css('.story-item > a::attr(href)').extract_first()
            item_hot = block.css('.story-item .top-notice .hot').extract_first()
            if item_hot:
                item_hot = True
            else:
                item_hot = False
            
            obj = ComicsItem(
                name=item_name,
                cover=item_cover,
                isHot=item_hot,
                url=item_url
            )
            yield obj

        time.sleep(3)
        for pagination in response.css(".pagination .pagination-list li"):
            next_html = pagination.css("a span::text").extract_first()
            if next_html and next_html == '›':
                next_url_path = pagination.css("a::attr(href)").extract_first()
                if next_url_path:
                    yield scrapy.Request(url=next_url_path, callback=self.parse)

        pass
