# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from crawl_be.items import ArticleItem, BookItem


class BeSpider(CrawlSpider):
    name = 'be'
    start_urls = ['http://www.xbiquge.la']

    rules = (
        Rule(LinkExtractor(allow=r'http://www.xbiquge.la/\d+?/\d+?/$'), callback='parse_item2', follow=True),
        Rule(LinkExtractor(allow=r'http://www.xbiquge.la/\d+?/\d+?/\d+?.html$'), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        item = ArticleItem()
        article_content = response.xpath('//div[@id="content"]').extract_first()
        article_title = response.xpath('//h1/text()').extract_first()
        book_title = response.xpath('//div[@class="con_top"]/a[3]/text()').extract_first()
        if article_title and article_content and book_title:
            item['title'] = article_title
            item['content'] = article_content
            item['book'] = book_title
            item['is_book'] = False
            yield item

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

