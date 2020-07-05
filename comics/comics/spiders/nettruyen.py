# -*- coding: utf-8 -*-
import scrapy
import time
import re
from datetime import datetime
from uuid import uuid4
from urllib.parse import unquote_plus
from comics.items import ComicsItem

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
            item_hot = block.css('.image .icon-hot').extract_first()
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

            time.sleep(0.3)
            yield scrapy.Request(url=item_url, callback=self.parse_detail)

        time.sleep(2)
        next_url_path = response.css(".pagination a.next-page::attr('href')").extract_first()
        if next_url_path:
            yield scrapy.Request(url=next_url_path, callback=self.parse)

        pass

    def parse_detail(self, response):
        item_name = response.css('#ctl00_divCenter h1.title-detail::text').extract_first()
        item_cover = response.css('#ctl00_divCenter .detail-info .col-image img::attr(src)').extract_first()
        item_altName = response.css('#ctl00_divCenter .detail-info .othername .other-name::text').extract_first()
        item_body = response.css('#ctl00_divCenter .detail-content p').extract_first()
        item_body = re.sub(r'<(.*?)>', '', item_body)
        item_body = re.sub(r'\xa0', '', item_body).strip()
        item_status = response.css('#ctl00_divCenter .detail-info .status .col-xs-8::text').extract_first()
        if item_status == "Đang tiến hành":
            item_status = 0
        else:
            item_status = 1
        item_categories = response.css('#ctl00_divCenter .detail-info .kind a::text').getall()
        item_authors = response.css('#ctl00_divCenter .detail-info .author a::text').getall()
        item_viewed = int(response.css('#ctl00_divCenter .detail-info li:last-child .col-xs-8::text').extract_first().replace('.', ''))
        item_followed = int(response.css('#ctl00_divCenter .follow b::text').extract_first().replace('.', ''))

        date_time_str = response.css('#item-detail time.small::text').extract_first()
        date_time_str = date_time_str.replace('[Cập nhật lúc: ', '')
        date_time_str = date_time_str.replace(']', '')
        item_updatedAt = datetime.strptime(date_time_str.strip(), '%H:%M %d/%m/%Y')

        yield({
            u'name': item_name,
            u'cover': item_cover,
            u'altName': item_altName,
            u'body': item_body,
            u'status': item_status,
            u'categories': item_categories,
            u'authors': item_authors,
            u'viewed': item_viewed,
            u'followed': item_followed,
            u'updatedAt': item_updatedAt
        })

        pass
