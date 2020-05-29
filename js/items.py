# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

class JsItem(scrapy.Item):
    author=scrapy.Field()
    content=scrapy.Field()
    url=scrapy.Field()
    title=scrapy.Field()
    authorlink=scrapy.Field()
    likes=scrapy.Field()
    comment=scrapy.Field()
    piclink=scrapy.Field()
    time=scrapy.Field()
    artical=scrapy.Field()
    article_id=scrapy.Field()