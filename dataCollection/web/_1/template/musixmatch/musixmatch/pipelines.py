# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


#class MusixmatchPipeline(object):
#    def process_item(self, item, spider):
#        return item

import json

class JsonExporterPipeline(object):
    def open_spider(self, spider):
        self.file = open('items.jl', 'w')

    def close_spider(self, spider):
        self.file.close()

    def process_item(self, item, spider):
        line = json.dumps(dict(item)) + "\n"
        self.file.write(line)
        return item


# %% push items to MongoDB
# ------------------------

# (from Scrapy official docu)

#import logging
#import pymongo

#class MongoPipeline(object):
#
#    collection_name = 'some_items'
#
#    def __init__(self, mongo_uri, mongo_db):
#        self.mongo_uri = mongo_uri
#        self.mongo_db = mongo_db
#
#    @classmethod
#    def from_crawler(cls, crawler):
#        ## pull in information from settings.py
#        return cls(
#            mongo_uri=crawler.settings.get('MONGO_URI'),
#            mongo_db=crawler.settings.get('MONGO_DATABASE')
#        )
#
#    def open_spider(self, spider):
#        ## initializing spider
#        ## opening db connection
#        self.client = pymongo.MongoClient(self.mongo_uri)
#        self.db = self.client[self.mongo_db]
#
#    def close_spider(self, spider):
#        ## clean up when spider is closed
#        self.client.close()
#
#    def process_item(self, item, spider):
#        ## how to handle each post
#        self.db[self.collection_name].insert(dict(item))
#        logging.debug("Item added to MongoDB")
#        return item
