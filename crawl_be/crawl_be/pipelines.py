# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import time

import psycopg2


class CrawlBePipeline(object):

    def open_spider(self, spider):
        host = 'localhost'
        user = 'postgres'
        pwd = '546452'
        db = 'book'
        self.conn = psycopg2.connect(host=host, user=user, password=pwd, dbname=db)
        self.cur = self.conn.cursor()
        self.cur.execute("SELECT title,id FROM book_book;")
        books = self.cur.fetchall()
        self.books = {i[0]: i[1] for i in books}

        self.cur.execute("SELECT title FROM book_article;")
        articles = self.cur.fetchall()
        self.articles = {i[0] for i in articles}

    def close_spider(self, spider):
        self.cur.close()
        self.conn.close()

    def process_item(self, item, spider):
        if item['is_book']:
            if item['title'] not in self.books.keys():
                self.cur.execute("INSERT INTO book_book(title, img_url, auth, date_created, date_updated) VALUES(%s, %s, %s, CURRENT_DATE, CURRENT_TIMESTAMP);", (item['title'], item['img_url'], item['auth']))
                self.conn.commit()
        else:
            if item['title'] not in self.articles:
                book_id = self.books.get(item['book'], None)
                self.cur.execute("INSERT INTO book_article(title, content, book_id, date_created, date_updated, book_title) VALUES(%s, %s, %s, CURRENT_DATE, CURRENT_TIMESTAMP, %s);", (item['title'], item['content'], book_id, item['book']))
                self.conn.commit()
