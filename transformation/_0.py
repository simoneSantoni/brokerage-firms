#!/usr/bin/env python3

"""
Docstring
------------------------------------------------------------------------------

------------------------------------------------------------------------------

Author: Simone Santoni, simone.santoni.1@city.ac.uk

Edits:
    - created
    - last edit

Notes: NaN

"""

# %% load libraries
# basic operations
import os
import json
import re
import logging
import time
import pickle
# load data from mongodb
from pymongo import MongoClient
# data analysis/management/manipulation
import numpy as np
import pandas as pd
# topic modeling
import gensim
from gensim.corpora import Dictionary
# nlp pipeline
import spacy
import en_core_web_lg


# %% Are libraries up-to-date? NLP libraries are in continuous flux!
print("""spaCy version: {}
      Gensim version: {}
      """.format(spacy.__version__, gensim.__version__))


# %% Read data

# create client
uri = "mongodb://simone:DELL123@10.16.142.91/default_db?authSource=admin"
client = MongoClient(uri)

# pick-up db
db = client.digitalTechs

# load the data
df = pd.DataFrame(list(db.find()))


# %% clean data

# basic cleaning
# -- date as datetime
df.loc[:, 'date'] = pd.to_datetime(df['date.$date'])
# -- get timespans
df.loc[:, 'year'] = df['date'].dt.year
# -- drop column
df.drop(['date.$date', '_id.$oid'], axis=1, inplace=true)
# -- remove returns
df.loc[:, 'text'] = df['text'].str.replace('\n', '')

# arrange data for sequential lda
# -- order data by year of publication
df.sort_values('year', inplace=true)
# -- get stacks by year
data = df.groupby('year').size()
# -- time slices
time_slices = data.values

# prepare list to pass through spacy
docs = [article.strip().lower() for article in df.text]

# hyphen to underscores
DOCS = [re.sub(r'\b-\b', '_', text) for text in DOCS]


# %% exploratory data analysis

# barchart of the distribution of articles over time
# -- data series
x = data.index
y = time_slices
# -- labels
x_labels = ['%s' % i for i in x if i < 2019] + ['2019*']
y_labels = ['%s' % i for i in np.arange(0, 1400, 200)]
# -- create figure
plt = plt.figure(figsize=(6, 4))
# -- populate figure with a plot
ax = plt.add_subplot(1, 1, 1)
# -- plot data
ax.bar(x, y, color='r', alpha=0.5)
# -- axis properties
ax.set_xticks(x)
ax.set_xticklabels(x_labels, fontsize=14, rotation='vertical')
ax.set_xlabel('year', fontsize=14)
ax.set_yticklabels(y_labels, fontsize=14)
ax.set_ylabel('counts of documents', fontsize=14)
# -- annotation
notes = """notes: * the 2019 bucket contains documents published
              between jan-01 and mar-31."""
plt.text(0.12, -0.25, notes, fontsize=12)
# -- grid
ax.grid(true, ls='--', axis='y', color='white')
# -- save plot
plt.savefig('barchart.pdf')


# %% NLP pipeline

# load spaCy model 'web_lg'
nlp = en_core_web_lg.load()

# expand on spaCy's stopwords
# -- my stopwrods
MY_STOPWORDS = ['\x1c',
                'ft', 'wsj', 'time', 'sec',
                'say', 'says', 'said',
                'mr.', 'mister', 'mr', 'miss', 'ms',
                'inc']
# -- expand on spaCy's stopwords
for stopword in MY_STOPWORDS:
    nlp.vocab[stopword].is_stop = True

# tokenize text
DOCS_TOKENS, TMP_TOKENS = [], []

for doc in DOCS:
    TMP_TOKENS = [token.lemma_ for token in nlp(doc)
                  if not token.is_stop
                  and not token.is_punct
                  and not token.like_num
                  and not token.like_url
                  and not token.like_email
                  and not token.is_currency
                  and not token.is_oov]
    DOCS_TOKENS.append(TMP_TOKENS)
    TMP_TOKENS = []

# take into account bi- and tri-grams
# -- get rid of common terms
COMMON_TERMS = [u'of', u'with', u'without', u'and', u'or', u'the', u'a',
                u'not', 'be', u'to', u'this', u'who', u'in']
# -- find phrases as bigrams
BIGRAM = Phrases(DOCS_TOKENS,
                 min_count=50,
                 threshold=5,
                 max_vocab_size=50000,
                 common_terms=COMMON_TERMS)
# -- fing phrases as trigrams
TRIGRAM = Phrases(BIGRAM[DOCS_TOKENS],
                  min_count=50,
                  threshold=5,
                  max_vocab_size=50000,
                  common_terms=COMMON_TERMS)

# uncomment if bi-grammed, tokenized document is preferred
#DOCS_PHRASED = [BIGRAM[line] for line in DOCS_TOKENS]

# check outcome of nlp pipeline
print('''
=============================================================================
Published article: {}

=============================================================================
Tokenized article: {}

=============================================================================
Tri-grammed tokenized article: {}

'''.format(DOCS[1],
           DOCS_TOKENS[1],
           DOCS_PHRASED[1])


# %% get corpus & dictionary to use for further NLP analysis

# get dictionary and corpus
DICT = Dictionary(DOCS_PHRASED)
CORPUS = [DICT.doc2bow(doc) for doc in DOCS_PHRASED]

# write dictionary and corpus to files


