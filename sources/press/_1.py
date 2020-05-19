#!/usr/bin/python3

"""
-------------------------------------------------------------------------------
                         CREATE CORPUS OF TEXT
-------------------------------------------------------------------------------

Author: Simone Santoni, simone.santoni.1@city.ac.uk

Dates:
    - created Mon Apr 15 10:02:46 UTC 2019
    - revise --

Notes: this should be re-run with dell_1

"""

# %% load libraries

import os
import glob
import pickle
import pandas as pd


# %% read files

SRV = '/media/simone/data'
PATH = 'Dropbox/dataProjects/code/AI/pressRelease/factiva/'
# AI-related articles
#FOLDER = '70d990e8-5e9d-11e9-9534-91cda7545daf'
# blockchain-related articles
FOLDER = 'b11148e2-98f7-11e9-92d0-8c859092e3b0'


#TODO: the folder should be moved to dell_1/dataDirectory

ARTICLES = glob.glob(os.path.join(SRV, PATH, FOLDER, '*.pickle'))


# %% tie data together

DF = []

for article in ARTICLES:
       with open(article, 'rb') as pipe:
              to_append = pickle.load(pipe)
       DF.append(to_append)


# get
DF = pd.DataFrame(DF)

# rename and index
DF.rename(columns={0: 'document_id',
                   1: 'title',
                   2: 'attributes',
                   3: 'text'},
          inplace=True)

DF.set_index('document_id', inplace=True)


# %% get date

DF.loc[DF['attributes'].str.contains('2017'), 'year'] =  2017
DF.loc[DF['attributes'].str.contains('2018'), 'year'] =  2018

DF = DF.loc[DF['year'].notnull()]


# %% serialize individual fields

# serialize attributes
#ATT = DF['attributes'].str.split('\n', expand=True)
#ATT.reset_index(inplace=True)
#ATT = ATT.melt(id_vars='document_id')
#ATT.set_index('document_id', inplace=True)
#
## serialize titles
#TI = DF['title'].str.split('\n', expand=True)
#TI.reset_index(inplace=True)
#TI = TI.melt(id_vars='document_id')
#TI.set_index('document_id', inplace=True)
#
## housekeeping
#DF.drop('attributes', axis=1, inplace=True)
#DF.drop('title', axis=1, inplace=True)
#TXT = DF


# %% double check text

#TXT.loc[:, 'text_len'] = TXT['text'].str.len()
#
## empty records
#TXT = TXT.loc[TXT['text_len'] > 0]
#
## document reference number records/urls
#TXT = TXT.loc[TXT['text_len'] > 100]
#
## rule of thumb for articles
#TXT = TXT.loc[TXT['text_len'] > 1000]


# %% write corpus of text

#for article in TXT.index:
#    text = TXT.loc[article, 'text']
#    out = article + '.txt'
#    folder = '108966fa-9980-11e9-90f7-f8b156d0a52b'
#    write = os.path.join(SRV, PATH, folder, out)
#    with open(write, 'wb') as pipe:
#        pipe.write(text)

FOLDER = '002787c0-99a7-11e9-90f7-f8b156d0a52b'
TARGET = os.path.join(SRV, PATH, FOLDER, 'blockchain_articles.csv')
DF.to_csv(TARGET, index=False)
