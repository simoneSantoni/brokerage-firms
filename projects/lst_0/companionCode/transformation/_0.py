#!/usr/bin/env python3

"""
Docstring
------------------------------------------------------------------------------
    _0.py    |    Creating a corpus and dictionary out of press data
------------------------------------------------------------------------------

Author: Simone Santoni, simone.santoni.1@city.ac.uk

Edits:
       - created
       - last edit

Notes: the dataset contains 4,384 articles published in the Wall Street
       Journal and the Financial Times that mention one or multiple
       of the following keywords:

       + Computer Software
       + Internet of Things
       + Machine Learning
       + Robotics
       + Technology
       + Computer Science
       + Computers
       + Automation
       + Augmented Reality
       + Big Data
       + Deep Learning
       + Cloud Computing
       + Natural Language Processing
       + Pattern Recognition
       + Analytics
       + Computing

"""

# %% load libraries
# basic operations
import os
import pickle
import re
# load data from mongodb
from pymongo import MongoClient
# data analysis/management/manipulation
import pandas as pd
# nlp pipeline
import spacy
import en_core_web_lg
# building corpus/dictionary
import gensim
from gensim.models import Phrases
from gensim.corpora import Dictionary, MmCorpus


# %% check software versions
print("""
spaCy version : {}
Gensim version: {}
""".format(spacy.__version__, gensim.__version__))


# %% work directory
srv = '/home/simone'
prj = 'githubRepos/digital-leadership-center'
fdr = 'scripts/transformation'
wd = os.path.join(srv, prj, fdr)
os.chdir(wd)


# %% read data

# create client
uri = ''
client = MongoClient()

# pick-up db
db = client.digitalTechs

# load the data
df = pd.DataFrame(list(db.press_releases.find()))


# %% clean data

# basic cleaning
# --+ get timespans
df.loc[:, 'year'] = df['date'].dt.year
# --+ slice the data
'''
let's focus on the 2013 - 2019 timespan, which concentrates the large majority
of the data.
'''
df = df.loc[df['year'] >= 2013]
# --+ drop column
df.drop('_id', axis=1, inplace=True)

# arrange data for sequential lda
# --+ order data by year of publication
df.sort_values('year', inplace=True)
# --+ get stacks by year
data = df.groupby('year').size()
# --+ time slices
time_slices = data.values
out_f = os.path.join('.data', 'pr_time_slices.txt')
with open(out_f, 'w') as pipe:
    for item in time_slices:
        pipe.write('{}\n'.format(item))

# prepare list to pass through spacy
docs = [article.strip().lower().replace('\n',' ') for article in df.text]

# hyphen to underscores
docs = [re.sub(r'\b-\b', '_', text) for text in docs]


# %% NLP pipeline

# load spaCy model 'web_lg'
nlp = en_core_web_lg.load()

# expand on spaCy's stopwords

# --+ my stopwrods
my_stopwords = ['\x1c',
                'ft', 'wsj', 'time', 'sec',
                'say', 'says', 'said',
                'mr.', 'mister', 'mr', 'miss', 'ms',
                'inc',
                '  ', '--', '---',
                'new', 'year', 'years',
                'join',
                'accord', 'accords',
                'u.s.', 'u.s',
                'cent', 'cents', 'trump'
                ]

# --+ expand on spacy's stopwords
for stopword in my_stopwords:
    nlp.vocab[stopword].is_stop = True

# tokenize text

# --+ containers
docs_tokens, tmp_tokens = [], []

# --+ nlp pipeline - iterate over documents
for doc in docs:
    tmp_tokens = [token.lemma_ for token in nlp(doc)
                  if not token.is_stop
                  and not token.is_punct
                  and not token.like_num
                  and not token.like_url
                  and not token.like_email
                  and not token.is_currency
                  and not token.is_space
                  and not token.is_oov]
    docs_tokens.append(tmp_tokens)
    tmp_tokens = []

# take into account bi- and tri-grams
# --+ get rid of common terms
common_terms = [u'of', u'with', u'without', u'and', u'or', u'the', u'a',
                u'not', 'be', u'to', u'this', u'who', u'in']
# --+ fing phrases as bigrams
bigram = Phrases(docs_tokens,
                 min_count=50,
                 threshold=5,
                 max_vocab_size=50000,
                 common_terms=common_terms)
# --+ fing phrases as trigrams
trigram = Phrases(bigram[docs_tokens],
                  min_count=50,
                  threshold=5,
                  max_vocab_size=50000,
                  common_terms=common_terms)
# NOTE: uncomment if a tri-grammed, tokenized document is preferred
docs_phrased = [bigram[line] for line in docs_tokens]
#docs_phrased = [trigram[bigram[line]] for line in docs_tokens]
# --+ write docs phrased to pickle
out_f = os.path.join('.data', 'pr_docs_phrased.pickle')
with open(out_f, 'wb') as pipe:
    pickle.dump(docs_phrased, pipe)

# check outcome of nlp pipeline
print('''
=============================================================================
published article:
-----------------------------------------------------------------------------
{}
=============================================================================
tokenized article:
-----------------------------------------------------------------------------
{}
=============================================================================
tri-grammed tokenized article:
-----------------------------------------------------------------------------
{}
'''.format(docs[1],
           docs_tokens[1],
           docs_phrased[1]))


# %% get corpus & dictionary to use for further nlp analysis

# get dictionary and write it to a file
pr_dictionary = Dictionary(docs_phrased)
pr_dictionary.save('.data/pr_dictionary.dict')

# get corpus and write it to a file
pr_corpus = [pr_dictionary.doc2bow(doc) for doc in docs_phrased]
out_f = os.path.join('.data', 'pr_corpus.mm')
MmCorpus.serialize(out_f, pr_corpus)
mm = MmCorpus(out_f) 
