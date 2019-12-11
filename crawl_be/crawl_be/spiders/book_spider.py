# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from crawl_be.items import BookItem


class BookSpider(CrawlSpider):
    name = 'book_spider'
    start_urls = ['http://www.xbiquge.la']

    rules = (
        Rule(LinkExtractor(allow=r'http://www.xbiquge.la/\d+?/\d+?/$'), callback='parse_item2', follow=True),
    )

    def parse_item2(self, response):
        item = BookItem()
        cover = response.xpath('//div[@id="fmimg"]/img/@src').extract_first()
        book_title = response.xpath('//h1/text()').extract_first()
        auth = response.xpath('//div[@id="info"]/p[1]/text()').extract_first().split('：')[1]
        if book_title and auth:
            item['title'] = book_title
            item['img_url'] = cover
            item['auth'] = auth
            item['is_book'] = True
            yield item

