#!/usr/bin/env python
# coding: utf-8

"""
-------------------------------------------------------------------------------
                SEMANTIC NETWORK ANALYSIS ON PRESS RELEASE DATA
                     -- AI/data science related articles --
-------------------------------------------------------------------------------

Author: Simone Santoni, simone.santoni.1@city.ac.uk

Dates: created Thu Aug  1 07:27:03 UTC 2019 – revised

Notes: None
"""


# %% load libraries
# --------------

# utilities
import os
import logging
import time
from pprint import pprint as pp
from collections import Counter

# data analysis/management/manipulation
import numpy as np
import scipy as sp
import pandas as pd

# nlp
import spacy
import en_core_web_lg
nlp = en_core_web_lg.load()
from spacy.matcher import Matcher
import gensim
from gensim.models import Phrases


# %% console settings
#    ----------------

# send output to the screen
line = ''.join(['\n', 79 * '-', '\n'])


# %% software version
# check libraries
print(' | '.join(['Numpy version: %s' % (np.__version__),
                  'Scipy version: %s' % (sp.__version__),
                  'spaCy version: %s' % (spacy.__version__)]),
      end=line)

# coding style
print('Coding style as per PEP8', '', end=line)


# %% rule-based matching
#    -------------------

'''
Rule-based matching should be seem, to a certain extent,
as an alternative to training a specific model of language.

Performance tip: run nlp.make_doc to speed things up
-----------------------------------
terms = [u"Barack Obama", u"Angela Merkel", u"Washington, D.C."]
patterns = [nlp.make_doc(text) for text in terms]
matcher.add("TerminologyList", None, *patterns)

# test matcher
test_doc = nlp(u'Deep learning does not have a clear role in the financial '\
                'sector is not clear yet')

matches = matcher(test_doc)
'''

def get_matches(docs_, ids_, pattern_, labels_):
    '''
    :param doc: factiva documents
    :param patterns: focal token combinations
    :return: list
    '''

    # matcher
    matcher = Matcher(nlp.vocab)

    # expand matcher
    for pattern, label in zip(pattern_, labels_):
        matcher.add(label, None, pattern)

    # containers
    my_matches = []

    # get matches
    for id, doc in zip(ids_, docs_):

        # nlp pipeline
        tokenized_ = nlp(doc)

        # find matches
        matches_ = matcher(tokenized_)

        # arrange matches
        if len(matches_) > 0:
            for match_id, start, end in matches_:
                string_id = nlp.vocab.strings[match_id]
                my_matches.append([id, len(tokenized_), match_id, string_id,
                                   start, end])
        else:
            pass

    return my_matches


# %% deploy function over AI data
#    ----------------------------

# read data
srv = '/media/simone/data'
path = 'Dropbox/dataProjects/code/DTLM/pressRelease/factiva'
folder = '002787c0-99a7-11e9-90f7-f8b156d0a52b'
in_f = 'ai_articles.csv'
df = pd.read_csv(os.path.join(srv, path, folder, in_f),
                 encoding='ISO-8859-1')
df.loc[:, 'id'] = np.arange(0, len(df))

# slice text corpus
condition = (df['year'] >= 2017) & (df['text'].notnull())
ai_docs = df.loc[condition, 'text'].to_list()
ai_docs = [str(i).replace('\n', '') for i in ai_docs]
ai_docs_id = df.loc[condition, 'id'].to_list()

# pattern
pattern = [[{'LOWER': 'artificial'}, {'LOWER': 'intelligence'}],
           [{'LOWER': 'deep'}, {'LOWER': 'learning'}],
           [{'LOWER': 'machine'}, {'LOWER': 'learning'}],
           [{'LOWER': 'big'}, {'LOWER': 'data'}],
           [{'LOWER': 'data'}, {'LOWER': 'analytics'}],
           [{'LOWER': 'natural'}, {'LOWER': 'language'}],
           [{'LOWER': 'processing'}]]

# labels
labels = ['AI', 'DL', 'ML', 'BigData', 'DataAnalytics', 'NLP']

# get function outcome
ai_matches = get_matches(ai_docs, ai_docs_id, pattern, labels)


# %% deploy function over blockchain data
#    ------------------------------------

# read data
srv = '/media/simone/data'
path = 'Dropbox/dataProjects/code/DTLM/pressRelease/factiva'
folder = '002787c0-99a7-11e9-90f7-f8b156d0a52b'
in_f = 'blockchain_articles.csv'
df = pd.read_csv(os.path.join(srv, path, folder, in_f),
                 encoding='ISO-8859-1')
df.loc[:, 'id'] = np.arange(0, len(df))

# slice text corpus
condition = (df['year'] >= 2017) & (df['text'].notnull())
bc_docs = df.loc[condition, 'text'].to_list()
bc_docs = [str(i).replace('\n', '') for i in bc_docs]
bc_docs_id = df.loc[condition, 'id'].to_list()

# pattern
pattern = [[{'LOWER': 'blockchain'}],
           [{'LOWER': 'cryptocurrency '}],
           [{'LOWER': 'peer-to-peer'}],
           [{'LOWER': 'encryption'}],
           [{'LOWER': 'bitcoin'}],
           [{'LOWER': 'distributed'}, {'LOWER': 'ledger'}]]

# labels
labels = ['BC', 'Cryptocurrency', 'P2P', 'Encryption', 'Bitcoing', 'DLDGR']

# get function outcome
bc_matches = get_matches(bc_docs, bc_docs_id, pattern, labels)



# %% function for semantic network analysis
#    --------------------------------------


def semantic_network(ego_lemmas, time_span):
    '''
    :param ego_lemmas: list of focal (ego) terms
    :param time_span: list with lower and upper bounds
    :return:
    '''

    # get docs
    docs_ = df.loc[((df['year'] >= time_span[0])
                    & (df['year'] <= time_span[1])
                    & (df['text'].notnull())), 'text'].to_list()

    # pass text through pipeline
    for doc_ in docs_[1:2]:
        tokens_ = nlp(doc_)

        # get lemma-lemma similarities
        for token_i in tokens_:
            for token_j in tokens_:
                print(token_i, token_j, token_i.similarity(token_j))



# %% locate hot terms using bigrams and trigrams
#    -------------------------------------------

#TODO: bigrams/trigrams approach

        # filtering tokens to store
        tokens_ = [token.lemma_ for token in tokens_
                   if not token.is_stop and not token.is_punct
                   and not token.like_num]

        # get rid of common terms
        common_terms = [u'of', u'with', u'without', u'and', u'or', u'the',
                        u'a', u'not', 'be', u'to', u'this', u'who', u'in']

        # find phrases
        bigram_ = Phrases(tokens_,
                          min_count=50,
                          threshold=5,
                          max_vocab_size=50000,
                          common_terms=common_terms)

        trigram_ = Phrases(bigram_[tokens_],
                           min_count=50,
                           threshold=5,
                           max_vocab_size=50000,
                           common_terms=common_terms)

        # uncomment if bi-grammed, tokenized document is preferred
        # docs_phrased = [bigram[line] for line in tokens]
        docs_phrased = [trigram_[bigram_[line]] for line in [tokens_]]
        # get term freqs
        instances_ = [i for i in docs_phrased[0] if i in ego_lemmas]
        if len(instances_) > 0:
            counts_ = Counter(instances_)
        else:
            pass


#TODO: semantic network analysis

# %% write data to files
#    -------------------


