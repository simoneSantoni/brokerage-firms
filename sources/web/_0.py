#!/usr/bin/python3

"""
Docstring

------------------------------------------------------------------------------
    _0.py    |    collect company - keywords instances with Google
------------------------------------------------------------------------------

Author: Simone Santoni, simone.santoni.1@city.ac.uk

Edits:
    - created
    - last change

Notes: NaN

"""

# %% load libraries
import os
import glob
import pickle
from time import sleep
from typing import List
import requests
import re
from urllib.parse import urlparse
from bs4 import BeautifulSoup as bs
import numpy as np
import pandas as pd
from pymongo import MongoClient


# %% setup
srv = '/home/simone'
prj = 'githubRepos/digital-leadership-center/sources'
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
    _hrefs: List[str] = []
    # clean query
    _query = '+'.join(['+OR+'.join(['%22{}%22'.format(i) for i in _keywords]),
                       '%22{}%22'.format(_entity),
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
        # write soup as text
        out_f = '{}_{}_soup.txt'.format(_entity, _after + 1)
        with open(out_f, 'w') as _pipe:
            _pipe.write(str(_soup.get_text()))
        # write soup as html
        out_f = '{}_{}_soup.html'.format(_entity, _after + 1)
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
                if (re.search('googleusercontent.com', _domain.netloc)):
                    continue
                else:
                    _hrefs.append(_rul)
            except:
                continue
        out_f = '{}_{}_hrefs.pickle'.format(_entity, _after + 1)
        with open(out_f, 'wb') as _pipe:
            pickle.dump(_hrefs, _pipe)
    else:
        pass


# %% run function 

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

# pick-up directory
os.chdir(os.path.join(cd, 'web/.data'))

# Crawlera proxy
proxy_host = "proxy.crawlera.com"
proxy_port = "8010"
proxy_auth = "24f6d103004d4ff1986826fb94a2c704:"
proxies = {"https": "https://{}@{}:{}/".format(proxy_auth, proxy_host, proxy_port),
           "http": "http://{}@{}:{}/".format(proxy_auth, proxy_host, proxy_port)}

# iterate over entities and timespans
for entity in entities[3:]:
    for i in np.arange(2009, 2020, 1):
        google_search(_proxy=proxies,
                      _entity=entity,
                      _keywords=keywords,
                      _after=i,
                      _before=i + 2)


# %% load lists with results

# scan for files
in_files = glob.glob('*.pickle')

# parse data
# -- empty list
urls = []
# -- iterate over files
for f in in_files:
    # company
    company = f.split('_')[0]
    # year
    year = f.split('_')[1]
    # open pipeline
    pipe = open(f, 'rb')
    # populate list with urls
    for item in pickle.load(pipe):
        urls.append([company, year, item])
    # close pipeline
    pipe.close()


# get Pandas df
df = pd.DataFrame(urls, columns=['company', 'year', 'url'])
# -- set index
#df.set_index(['company', 'year'], inplace=True)

# %% send data to mongo

# open client
client = MongoClient()

# pick-up db
db = client.digitalTechs

# push data via bulk insert
db.web_search.insert_many(df.to_dict('records'))

