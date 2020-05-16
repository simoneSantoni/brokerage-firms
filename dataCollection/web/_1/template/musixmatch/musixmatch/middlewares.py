# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

#from scrapy import signals
#
#
#class MusixmatchSpiderMiddleware(object):
#    # Not all methods need to be defined. If a method is not defined,
#    # scrapy acts as if the spider middleware does not modify the
#    # passed objects.
#
#    @classmethod
#    def from_crawler(cls, crawler):
#        # This method is used by Scrapy to create your spiders.
#        s = cls()
#        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
#        return s
#
#    def process_spider_input(self, response, spider):
#        # Called for each response that goes through the spider
#        # middleware and into the spider.
#
#        # Should return None or raise an exception.
#        return None
#
#    def process_spider_output(self, response, result, spider):
#        # Called with the results returned from the Spider, after
#        # it has processed the response.
#
#        # Must return an iterable of Request, dict or Item objects.
#        for i in result:
#            yield i
#
#    def process_spider_exception(self, response, exception, spider):
#        # Called when a spider or process_spider_input() method
#        # (from other spider middleware) raises an exception.
#
#        # Should return either None or an iterable of Request, dict
#        # or Item objects.
#        pass
#
#    def process_start_requests(self, start_requests, spider):
#        # Called with the start requests of the spider, and works
#        # similarly to the process_spider_output() method, except
#        # that it doesn’t have a response associated.
#
#        # Must return only requests (not items).
#        for r in start_requests:
#            yield r
#
#    def spider_opened(self, spider):
#        spider.logger.info('Spider opened: %s' % spider.name)
#
#
#class MusixmatchDownloaderMiddleware(object):
#    # Not all methods need to be defined. If a method is not defined,
#    # scrapy acts as if the downloader middleware does not modify the
#    # passed objects.
#
#    @classmethod
#    def from_crawler(cls, crawler):
#        # This method is used by Scrapy to create your spiders.
#        s = cls()
#        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
#        return s
#
#    def process_request(self, request, spider):
#        # Called for each request that goes through the downloader
#        # middleware.
#
#        # Must either:
#        # - return None: continue processing this request
#        # - or return a Response object
#        # - or return a Request object
#        # - or raise IgnoreRequest: process_exception() methods of
#        #   installed downloader middleware will be called
#        return None
#
#    def process_response(self, request, response, spider):
#        # Called with the response returned from the downloader.
#
#        # Must either;
#        # - return a Response object
#        # - return a Request object
#        # - or raise IgnoreRequest
#        return response
#
#    def process_exception(self, request, exception, spider):
#        # Called when a download handler or a process_request()
#        # (from other downloader middleware) raises an exception.
#
#        # Must either:
#        # - return None: continue processing this exception
#        # - return a Response object: stops process_exception() chain
#        # - return a Request object: stops process_exception() chain
#        pass
#
#    def spider_opened(self, spider):
#        spider.logger.info('Spider opened: %s' % spider.name)

# Below are two custom middlewares
# ---------------------------------

from scrapy import signals
from toripchanger import TorIpChanger

# Rotate ips with toripchanger
# ----------------------------

ip_changer = TorIpChanger(tor_password='my password',
                          tor_port=9051,
                          local_http_proxy='127.0.0.1:8118',
                          reuse_threshold=10)


class TorIpProxyMiddleware(object):
    _requests_count = 0

    def process_request(self, request, spider):
        self._requests_count += 1

        if self._requests_count > 10:
            self._requests_count = 0
            ip_changer.get_new_ip()

        request.meta['proxy'] = 'http://127.0.0.1:8118'
        #spider.log('Proxy : %s' % request.meta['proxy'])


# Rotate ips with stem
# --------------------

from stem import Signal
from stem.control import Controller
import requests


def retrieve_ip():
    # get info (IP...) from current connection
    session = requests.session()
    # Tor uses the 9050 port as the default socks port. You use it if you want to proxy something through Tor
    session.proxies = {
        'http': 'socks5://127.0.0.1:9050',
        'https': 'socks5://127.0.0.1:9050'
    }

    return session


def set_new_ip():
    with Controller.from_port(port=9051) as controller:
        controller.authenticate(password="my password")
        controller.signal(Signal.NEWNYM)


class StemProxyMiddleware(object): 
    def process_request(self, request, spider):
        '''
        > short version: replace everything in this def by:
        set_new_ip()
        request.meta['proxy'] = 'http://127.0.0.1:8118'
        > long verion :
        the print display the IP address, to show that Tor change it
        '''
        print("\n\nProxyMiddleware: Start")
        site = 'http://httpbin.org/ip'

        # get public IP
        print("my normal public IP", requests.get(site).text)

        # get Tor IP
        my_ip = retrieve_ip()
        print("IP visible through Tor(request)", my_ip.get(site).text)

        # change IP, retrieve it to print it
        set_new_ip()  # ask Tor to change IP
        my_ip = retrieve_ip()
        print("IP visible through Tor (stem)", my_ip.get(site).text)

        # get request from spider and ask it to go through a proxy (privoxy = 'http://127.0.0.1:8118'  - privoxy acts like a man-in-the-middle in the computer
        request.meta['proxy'] = 'http://127.0.0.1:8118'
        print("proxy used: ", request.meta['proxy'])

        print("\n\nProxyMiddleware: End")
