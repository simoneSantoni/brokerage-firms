# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field

class GsearchItem(Item):
    name = Field()
    region = Field()
    url = Field()
    html = Field()
    query = Field()
    crawled = Field()
