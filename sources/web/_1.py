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
import requests
import re
import bs4
from pymongo import MongoClient
import pandas as pd


# %% mongo pipeline
client = MongoClient()
db = client.digitalTechs


# %% define function to crawl (and push data to mongo)

# custom function
def crawl_and_push(_url, _entity, _year):
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
            # return list
            #return [_url, _text]
            # push text to mongo
            db.web_contents.insert_one({'entity': _entity,
                                        'year': _year,
                                        'url': _url,
                                        'content': _text})
        else:
            pass
    except:
        pass


# %% run function

# get target urls
urls = list(db.web_search.find())

# get Pandas df
df = pd.DataFrame(urls)

targets = [[item['company'], item['year'], item['url']] for item in urls]

# -- filter out ads
targets = [item for item in targets if 'googlead' not in item[2]]
targets = [item for item in targets if'cloudera' not in item[2]]
targets = [item for item in targets if'oracle' not in item[2]]
targets = [item for item in targets if'sas.com' not in item[2]]
targets = [item for item in targets if'linkedin.com' not in item[2]]
targets = [item for item in targets if'qubole.com' not in item[2]]
targets = [item for item in targets if'ibm.com' not in item[2]]
targets = [item for item in targets if'glassdoor.com' not in item[2]]
targets = [item for item in targets if'intel.com' not in item[2]]
targets = [item for item in targets if'amazon.com' not in item[2]]
# -- filter out long files
targets = [item for item in targets if'.pptx' not in item[2]]
targets = [item for item in targets if'.docx' not in item[2]]
targets = [item for item in targets if'.xlsx' not in item[2]]
targets = [item for item in targets if'.ppt' not in item[2]]
targets = [item for item in targets if'.doc' not in item[2]]
targets = [item for item in targets if'.xls' not in item[2]]
targets = [item for item in targets if'.pdf' not in item[2]]
targets = [item for item in targets if'.zip' not in item[2]]
targets = [item for item in targets if'.tar.gz' not in item[2]]
targets = [item for item in targets if'.xml.gz' not in item[2]]

# run function
for entity, year, url in targets:
    crawl_and_push(_entity=entity,
                   _year=year,
                   _url=url)

