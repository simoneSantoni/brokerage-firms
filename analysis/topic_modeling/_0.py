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
import pickle
import matplotlib.pyplot as plt
import gensim
from gensim.models import ldaseqmodel
from gensim.corpora import Dictionary, MmCorpus


# %% set working dir
srv = '/home/simone'
prj = 'githubRepos/digital-leadership-center'
fdr = 'analysis/topicModeling'
wd = os.path.join(srv, prj, fdr)


# %% load data

# collection in Mongo

# %% read data

# collection in Mongo
# --+ open pipeline
client = MongoClient()
# --+ pick-up db
db = client.digitalTechs
# --+ load the data
df = pd.DataFrame(list(db.press_releases.find()))

# corpus and dictionary


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

# arrange data for sequential lda
# --+ order data by year of publication
df.sort_values('year', inplace=True)
# --+ get stacks by year
data = df.groupby('year').size()




# %% exploratory data analysis



# barchart of the distribution of articles over time
# --+ data series
x = data.index
y = time_slices
# --+ labels
x_labels = ['%s' % i for i in x if i < 2019] + ['2019*']
y_labels = ['%s' % i for i in np.arange(0, 1400, 200)]
# --+ create figure
fig = plt.figure(figsize=(6, 4))
# --+ populate figure with a plot
ax = fig.add_subplot(1, 1, 1)
# --+ plot data
ax.bar(x, y, color='r', alpha=0.5)
# --+ axis properties
ax.set_xticks(x)
ax.set_xticklabels(x_labels, fontsize=14, rotation='vertical')
ax.set_xlabel('year', fontsize=14)
ax.set_yticklabels(y_labels, fontsize=14)
ax.set_ylabel('counts of documents', fontsize=14)
# --+ annotation
notes = """notes: * the 2019 bucket contains documents published
              between Jan-01 and Mar-31."""
plt.text(0.12, -0.25, notes, fontsize=12)
# --+ grid
ax.grid(True, ls='--', axis='y', color='white')
# --+ save plot
#plt.show()
#folder = 'ss_1/exhibits'
plt.savefig('articles_by_year.pdf',
            transparent=True,
            bbox_inches='tight',
            pad_inches=0,
            dpi=600)