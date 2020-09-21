#!/usr/bin/python3

"""
Docstring
------------------------------------------------------------------------------
_1.py  |  creting corpus of text to upload to Mongo
------------------------------------------------------------------------------

Author: Simone Santoni, simone.santoni.1@city.ac.uk

Dates:
    - created Mon Apr 15 10:02:46 UTC 2019
    - revise

Notes: this should be re-run with dell_1

"""

# %% load libraries
import os
import glob
import pickle
import re
import pymongo
from pymongo import MongoClient
import pandas as pd


# %% set path to data
srv = '/media/simone'
dr = 'data/dataDirectory'
wd = os.path.join(srv, dr)
os.chdir(wd)


# %% scree for pickles containing individual articles

# folder/source
# fdr = '2b50f5c0-9cd6-11ea-9ed2-f8b156d0a52b'
# --+ data integrations
fdr = '7993c3e8-fb36-11ea-92fa-d9d41eab827b'
src = 'press'

# read files
in_files = glob.glob(os.path.join(fdr, src, '*.pickle'))

# stupid left_index
print(in_files)

# %% manage the corpus of text

# assign articles to a list
# -- empty list
articles = []
# -- iterate over pickles & append articles
'''
note: pickles have been created with Python 2.7
      -- cause: Python 3 doesn't go well with 'unrtf'
      -- solution: encoding has to be passed explicitely in pickle.load()
'''
for f in in_files:
       with open(f, 'rb') as pipe:
              to_append = pickle.load(pipe, encoding='latin1')
       articles.append(to_append)

# assign article to a Pandas df
# -- read list
col_names = ['document_id', 'title', 'attributes', 'text']
df = pd.DataFrame(articles, columns=col_names)
# -- set index
df.set_index('document_id', inplace=True)


# %% extract article attributes

# outlet
# -- empty list
outlet = []
# -- iterate over articles
for item in articles:
    # get id
    _id = item[0]
    # get attributes
    _attributes = item[2]
    # test for pattern matching
    # -- test for FT
    if b'Financial Times' in _attributes:
        outlet.append([_id, 'ft'])
    # test for WSJ
    elif (b'Wall Street Journal' in _attributes) or (b'WSJ' in _attributes):
        outlet.append([_id, 'wsj'])
    # test for The Economist
    elif b'The Economist' in _attributes:
        outlet.append([_id, 'te'])
    else:
        pass


# -- get Pandas df
col_names = ['document_id', 'outlet']
df_o = pd.DataFrame(outlet, columns=col_names)
# -- set index
df_o.set_index('document_id', inplace=True)

# date
# -- empty list
date = []
# -- iterate over articles
for item in articles:
    # get id
    _id = item[0]
    # get attributes
    _attributes = item[2]
    # pattern matching
    # -- find month (word) + day (digit) + year (digit)
    to_append = re.search(b"(\d+) (\w+) (\d+)", _attributes)
    if to_append is not None:
        date.append([_id, to_append.group(0)])
    else:
        pass


# -- get Pandas df
col_names = ['document_id', 'date']
df_d = pd.DataFrame(date, columns=col_names)
# -- set index
df_d.set_index('document_id', inplace=True)


# %% polish data

# merge with all the rest
df = pd.merge(df, df_o, left_index=True, right_index=True, how='inner')
df = pd.merge(df, df_d, left_index=True, right_index=True, how='inner')

# date cleaning
# -- text as string
df.loc[:, 'text'] = df['text'].str.decode('utf-8', errors='ignore')
df.loc[:, 'title'] = df['title'].str.decode('utf-8', errors='ignore')
# -- dates and datetimeco
df.loc[:, 'date'] = df['date'].str.decode('utf-8')
df.loc[:, 'date'] = pd.to_datetime(df['date'])
# -- drop redundant cols
df.drop('attributes', axis=1, inplace=True)

# quality check
df.loc[:, 'text_len'] = df['text'].str.len()
# -- focus on articles whose len is >= 1,000
df = df.loc[df['text_len'] >= 1000]


# %% write corpus of text to mongo

# open pipeline
client = MongoClient()

# pick-up db
db = client.digitalTechs

# bulk insert
db.press_releases.insert_many(df.to_dict('records'))
