# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ArticleItem(scrapy.Item):
    title = scrapy.Field()
    content = scrapy.Field()
    book = scrapy.Field()
    is_book = scrapy.Field()


class BookItem(scrapy.Item):
    title = scrapy.Field()
    img_url = scrapy.Field()
    auth = scrapy.Field()
    is_book = scrapy.Field()
