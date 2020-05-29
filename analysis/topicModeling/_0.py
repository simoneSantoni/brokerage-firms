#!/usr/bin/env python3

"""
Docstring
------------------------------------------------------------------------------
    _0.py    |    sequential LDA on press release-data
------------------------------------------------------------------------------

Author: Simone Santoni, simone.santoni.1@city.ac.uk

Edits:
       - created
       - last change

Notes: NaN

"""

# %% load libraries
import os
from pymongo import MongoClient
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rc
import pandas as pd
import gensim as gn
from gensim.corpora import Dictionary, MmCorpus
from gensim.models import ldaseqmodel


# %% set working dir
srv = '/home/simone'
prj = 'githubRepos/digital-leadership-center'
wd = os.path.join(srv, prj)
os.chdir(wd)


# %% viz options
plt.style.use('seaborn-bright')
rc('font',**{'family':'serif','serif':['Computer Modern Roman']})
rc('text', usetex=True)


# %% load data

# collection in Mongo
# --+ open pipeline
client = MongoClient()
# --+ pick-up db
db = client.digitalTechs
# --+ load the data
df = pd.DataFrame(list(db.press_releases.find()))

# dictionary
in_f = os.path.join('transformation', '.data', 'pr_dictionary.dict')
dictionary = Dictionary.load(in_f)

# corpus
in_f = os.path.join('transformation', '.data', 'pr_corpus.mm')
corpus = MmCorpus(in_f)

# time slices to pass to the sequential lda
in_f = os.path.join('transformation', '.data', 'pr_time_slices.txt')
time_slices = []
with open(in_f, 'rb') as pipe:
    for line in pipe.readlines():
        time_slices.append(int(line.strip()))

# %% clean data read from Mongo

# basic cleaning
# --+ get timespans
df.loc[:, 'year'] = df['date'].dt.year
# --+ slice the data
'''
let's focus on the 2013 - 2019 timespan, which concentrates the large majority
of the data.
'''
df = df.loc[df['year'] >= 2009]
# --+ drop column
df.drop(['_id'], axis=1, inplace=True)


# %% exploratory data analysis

# barchart of the distribution of articles over time
# --+ data series
x = np.arange(2013, 2020, 1)
y0 = df.loc[(df['outlet'] == 'ft') &
            (df['year'] >=2013)].groupby('year').size().values
y1 = df.loc[(df['outlet'] == 'wsj') &
            (df['year'] >= 2013)].groupby('year').size().values
# --+ labels
x_labels = ['%s' % i for i in x if i < 2019] + ['2019*']
y_labels = ['%s' % i for i in np.arange(0, 1400, 200)]
for i, s in enumerate(y_labels):
    if len(s) > 3:
        y_labels[i] = '{},{}'.format(s[0], s[1:])
    else:
        pass
# --+ create figure
fig = plt.figure(figsize=(6, 4))
# --+ populate figure with a plot
ax = fig.add_subplot(1, 1, 1)
# --+ plot data
ax.bar(x, y0, color='k', width=0.6, alpha=0.50, edgecolor='white',
       label='Financial Times')
ax.bar(x, y1, color='k', width=0.6, alpha=0.25, edgecolor='white', bottom=y0,
       label='Wall Street Journal')
# --+ axis properties
ax.set_xticks(x)
ax.set_xticklabels(x_labels, fontsize=14, rotation='vertical')
ax.set_xlabel('Year', fontsize=14)
ax.set_yticklabels(y_labels, fontsize=14)
ax.set_ylabel('Counts of documents', fontsize=14)
# --+ hide all spines while preserving ticks
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)
ax.spines['bottom'].set_visible(False)
ax.spines['left'].set_visible(False)
ax.yaxis.set_ticks_position('left')
ax.xaxis.set_ticks_position('bottom')
ax.yaxis.set_ticks_position('left')
ax.xaxis.set_ticks_position('bottom')
# --+ grid
ax.grid(True, ls='--', axis='y', color='white')
# --+ legend
plt.legend(loc='best')
# --+ save plot
out_f = os.path.join('analysis', 'topicModeling', '.output', '_0.pdf')
plt.savefig(out_f, bbox_inches='tight', pad_inches=0)


# %% dynamic topic modeling

random_state = np.random.seed(111)

lda_10 = ldaseqmodel.LdaSeqModel(corpus=corpus,
                                 id2word=dictionary,
                                 time_slice=time_slices,
                                 num_topics=10,
                                 random_state=random_state)
