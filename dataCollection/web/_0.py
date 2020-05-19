#!/usr/bin/python3

"""
DOCSTRING

------------------------------------------------------------------------------
    _0.py    |
------------------------------------------------------------------------------

Author: Simone Santoni, simone.santoni.1@city.ac.uk

Dates:
    - Created
    - Revised

Progress/TO DO:
    - use crawlera to make requests
    - randomize the order of the query
    - play with the timespan of the query
    - names of the companies should make sense for Google
    - use data on titles to screen for candidate sources


Here's the snippet of code to 

import requests

url = "http://httpbin.org/ip"
proxy_host = "proxy.crawlera.com"
proxy_port = "8010"
proxy_auth = "<APIKEY>:" # Make sure to include ':' at the end
proxies = {"https": "https://{}@{}:{}/".format(proxy_auth, proxy_host, proxy_port),
      "http": "http://{}@{}:{}/".format(proxy_auth, proxy_host, proxy_port)}

r = requests.get(url, proxies=proxies,
                 verify=False)

print('''
Requesting [{}]
through proxy [{}]

Request Headers:
{}

Response Time: {}
Response Code: {}
Response Headers:
{}

'''.format(url, proxy_host, r.request.headers, r.elapsed.total_seconds(),
           r.status_code, r.headers, r.text))

"""

# %% load libraries
import os
from time import sleep
from typing import List
import requests
import re
from urllib.parse import urlparse
from bs4 import BeautifulSoup as bs
import numpy as np
from toripchanger import TorIpChanger


# %% setup
srv = '/home/simone'
prj = 'githubRepos/digital-leadership-center/dataCollection'
cd = os.path.join(srv, prj)
os.chdir(cd)


# %% custom search function
def google_search(_entity,
                  _keywords,
                  _after,
                  _before,
                  _proxy,
                  _seed = 'https://www.google.com/search?client=ubuntu&channel=fs&q=',
                  target_n = 100):
    '''
    Docstring
    =========
    arguments
    ---------
    _seed     : the seed for the Google search
    _entity   : a string associated to the entity to search
    _keywords : a list of strings associated with an entity's attributes
    _after    : integer the identifies the lower bound of the timespan
    _before   : integer the identifies the upper bound of the timespan
    _proxy    : optional, the proxy request passes through
    target_n  : integer that identifies the number of results to display
                per page
    return
    ------
    _hrefs    : a list of the urls pointing to documents that are consistent
                with the query (i.e., _entity - _keywords pairs)
    '''
    # container
    #_hrefs: List[str] = []
    # clean query
    _query = '+'.join(['+OR+'.join(['%22{}%22'.format(i) for i in _keywords]),
                       '%22{}%22'.format(_entity.replace(' ', '+')),
                       'after%3A{}'.format(_after),
                       'before%3A{}'.format(_before)])
    # compose url
    _url = '{}{}&num={}&hl=en&gl=en&ie=utf-8'.format(_seed, _query, str(target_n))
    # notification
    print(
    """
    ====================================================================
    Working on `{}' / year {}
    --------------------------------------------------------------------
    """.format(_entity, _after + 1)
    )
    # make request and parse urls
    _html = requests.get(_url,
                         proxies=_proxy,
                         verify=False)
    if _html.status_code == 200:
        _soup = bs(_html.text, 'lxml')
        out_f = '{}_{}_soup.txt'.format(_entity, _after + 1)
        with open(out_f, 'w') as _pipe:
            _pipe.write(str(_soup))
        _a = _soup.find_all('a')
        for i in _a:
            k = i.get('href')
            try:
                m = re.search("(?P<url>https?://[^\s]+)", k)
                n = m.group(0)
                _rul = n.split('&')[0]
                _domain = urlparse(_rul)
                if (re.search('google.com', _domain.netloc)):
                    continue
                else:
                    _hrefs.append(_rul)
            except:
                continue
        out_f = '{}_{}_hrefs.txt'.format(_entity, _after + 1)
        with open(out_f, 'w') as _pipe:
            for item in _hrefs:
                _pipe.write('{}\n'.format(item))
        print("""Data have been written to {}""".format(out_f))
    else:
        pass


# %% operate function

# keywords
keywords = ['artificial+intelligence',
            'deep+learning',
            'machine+learning',
            'big+data',
            'natural+language+processing',
            'analytics']

# companies
'''
loading the names of the unique companies associated to the top 100 legal
entities included in the Bloomber export 
'''
with open(os.path.join('companies', 'top100_disambiguated.txt')) as pipe:
    entities = [i.rstrip() for i in pipe.readlines()]

# tor ip changer
# -- renew ip after one call
tor_ip_changer_1 = TorIpChanger(tor_password='my password',
                                tor_port=9051,
                                local_http_proxy='http://127.0.0.1:8118')


tor_ip_changer_1.get_new_ip()


# -- don't reuse an ip
tor_ip_changer_0 = TorIpChanger(tor_password='my password',
                                tor_port=9051,
                                local_http_proxy='http://127.0.0.1:8118',
                                reuse_threshold=0)
current_ip = tor_ip_changer_0.get_new_ip()

# pick-up directory
os.chdir(os.path.join(cd, '.data'))

# Crawlera proxy
proxy_host = "proxy.crawlera.com"
proxy_port = "8010"
proxy_auth = "24f6d103004d4ff1986826fb94a2c704:"
proxies = {"https": "https://{}@{}:{}/".format(proxy_auth, proxy_host, proxy_port),
           "http": "http://{}@{}:{}/".format(proxy_auth, proxy_host, proxy_port)}

# iterate over entities and timespans
for entity in entities[0:3]:
    # sleep(50)
    for i in np.arange(2009, 2019, 1):
        urls.append(google_search(_proxy=proxies,
                                  _entity=entity,
                                  _keywords=keywords,
                                  _after=i,
                                  _before=i + 2))
        print("""
        Searching [{}, {}]
        through proxy [{}]
        
        Request Headers:
        {}
        
        Response Time: {}
        Response Code: {}
        Response Headers:
        {}
        
        """.format(entity, i,
                   proxy_host, r.request.headers, r.elapsed.total_seconds(),
                   r.status_code, r.headers, r.text))
