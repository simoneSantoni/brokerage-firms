# -*- coding: utf-8 -*-
import scrapy
from scrapy.loader import ItemLoader
from broadcrawl.items import BroadcrawlItem

class SpiderSpider(scrapy.Spider):
    name = 'spider'
    #allowed_domains = ['example.com']
    start_urls = ['http://example.com/']

    def parse(self, response):
        l = ItemLoader(item=BroadcrawlItem(), response=response)
        l.add_xpath('contents', '//div[@class="product_name"]')
        return l.load_item()
