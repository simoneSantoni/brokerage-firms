#!/usr/env/bin python3

"""
Docstring
------------------------------------------------------------------------------
    _1.py |    crawl contents from individual pages
------------------------------------------------------------------------------

Author: Simone Santoni, simone.santoni.1@city.ac.uk

Edits:

    - created --
    - last change --

Notes: NaN

"""


# %% load libraries
import os
import requests
import eventlet
eventlet.monkey_patch()
import re
import bs4
from pymongo import MongoClient


# %% mongo pipeline
#client = MongoClient()
#db = client.digitalTechs


# %% define function to crawl (and push data to mongo)

# custom function
def crawl_and_push(_url):
    '''
    : argument: url, string
    : return  : url contents in .json format, pushed to mongo
    '''
    # request
    try:
        _r = requests.get(_url, timeout=3, verify=False)
        # make the soup
        if _r.status_code == 200:
            _soup = bs4.BeautifulSoup(_r.text, 'lxml')
            # get text
            _text = str(_soup.get_text())
            _text = re.sub(r'\n+', '\n', _text).strip()
            return [_url, _text]
            # push text to mongo
            #db.web_contents.insert_one({'url': _url, 'content': _text})
        else:
            pass
    except requests.exceptions.Timeout as e: 
        print(e)


# %% run function

# get target urls
urls = list(db.web_search.find())
target_urls = [item['url'] for item in urls]  
# -- filter out google ads
target_urls = [item for item in target_urls if 'googlead' not in item]
target_urls = [item for item in target_urls if 'cloudera' not in item]
target_urls = [item for item in target_urls if 'oracle' not in item]
target_urls = [item for item in target_urls if 'sas.com' not in item]
target_urls = [item for item in target_urls if 'linkedin.com' not in item]
target_urls = [item for item in target_urls if 'qubole.com' not in item]
target_urls = [item for item in target_urls if 'ibm.com' not in item]
target_urls = [item for item in target_urls if 'glassdoor.com' not in item]
# -- filter out long documents
target_urls = [item for item in target_urls if '.pptx' not in item]
target_urls = [item for item in target_urls if '.docx' not in item]
target_urls = [item for item in target_urls if '.xlsx' not in item]
target_urls = [item for item in target_urls if '.ppt' not in item]
target_urls = [item for item in target_urls if '.doc' not in item]
target_urls = [item for item in target_urls if '.xls' not in item]
target_urls = [item for item in target_urls if '.pdf' not in item]
target_urls = [item for item in target_urls if '.zip' not in item]
target_urls = [item for item in target_urls if '.tar.gz' not in item]


# run function
for item in target_urls:
    crawl_and_push(item)

