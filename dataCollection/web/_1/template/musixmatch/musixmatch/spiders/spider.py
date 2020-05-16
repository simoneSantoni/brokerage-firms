# -*- coding: utf-8 -*-
#import scrapy
#
#
#class SpiderSpider(scrapy.Spider):
#    name = 'spider'
#    allowed_domains = ['musixmatch.com']
#    start_urls = ['http://musixmatch.com/']
#
#    def parse(self, response):
#        pass

# %% libraries and modules
# ------------------------
#import datetime
import numpy as np
import scrapy
#from scrapy.loader import ItemLoader
#from scrapy.loader.processors import MapCompose#, Join
from musixmatch.items import MusixmatchItem
#from scrapy_splash import SplashRequest

# %% params for search
# --------------------

# base url
BASE_URL = 'https://www.musixmatch.com/track/'

# divide the task into batches
BATCH_SIZE = 100
MIN = 1389043
MAX = MIN + 100
TRACK_SET = np.arange(MIN, MAX, 1)

# %% spider class
# ---------------


class SpiderSpider(scrapy.Spider):
    name = 'spider'
    allowed_domains = ['musixmatch.com']

    # make request
    def start_requests(self):
        urls = [BASE_URL + str(i) for i in TRACK_SET]

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    # make request ad render target web page locally
    #def start_requests(self):
    #    for url in self.start_urls:

    #        # lua script
    #        script = """
    #            function main(splash)
    #                assert(splash:go(splash.args.url))
    #                splash:wait(0.5)
    #                return splash:html()
    #            end
    #            """

    #        # make request
    #        yield SplashRequest(url, self.parse, endpoint='execute',
    #                            args={'lua_source': script,},)

    # save stuff, items do not go through the pipeline
    #def parse(self, response):

    #    # file name
    #    rel_url = response.url.split("/")[-2]

    #    # response body
    #    #with open(out_f, 'wb') as f:
    #    #    f.write(response.body)

    #    #self.log('Saved file %s' % out_f)

    #    # .js stuff
    #    api = response.css('::text').re(r'_mxmState = \s*(.*)')[0].strip(';')
    #    extension = 'json'
    #    out_f = '.'.join([rel_url, extension])
    #    with open(out_f, 'wb') as pipe:
    #        pipe.write(api)
    #    self.log('Saved file %s' % out_f)

    # parser
    def parse(self, response):

        # create the loader using the response
        item = MusixmatchItem()
        #l = ItemLoader(item=MusixmatchItem(), response=response)
        # artist name
        js = response.css('::text').re(r'_mxmState = \s*(.*)')
        item['content'] = js[0].strip(';')

        # track url
        #item['url'] = response.url.split('.com/')[1]
        #l.add_value('url', '')

        # timestamp
        # l.add_value('date', datetime.datetime.now())

        # ip used for the request
        #item['ip'] = response.headers

        return item
        #yield l.load_item()
