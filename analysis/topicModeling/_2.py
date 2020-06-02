#!/usr/bin/env python3

"""
Docstring
------------------------------------------------------------------------------
    _2.py    |    statistical analysis of LDA results
------------------------------------------------------------------------------

Author: Simone Santoni, simone.santoni.1@city.ac.uk

Edits:
       - created
       - last change

Notes: This script deals with press-release .

"""


# %% load libraries
import os
from glob import glob
from pymongo import MongoClient
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import pandas as pd


# %% set working dir
srv = '/home/simone'
prj = 'githubRepos/digital-leadership-center'
wd = os.path.join(srv, prj)
os.chdir(wd)


# %% viz options
plt.style.use('seaborn-bright')
rc('font',**{'family':'serif','serif':['Computer Modern Roman']})
rc('text', usetex=True)


# %% document attributes

# open pipeline
client = MongoClient()
# pick-up db
db = client.digitalTechs
# load the data
df = pd.DataFrame(list(db.press_releases.find()))
# cleaning
df.loc[:, 'year'] = df['date'].dt.year 
# slice data
df = df.loc[df['year'] >= 2013]


# %% data to visualize

# screen for all .csv that are byproduct of topic modeling
in_fs = glob(os.path.join('analysis', 'topicModeling', '.output', '*.csv'))

# manipulate

# --+ 8 topic model
# ----+ doc2topic probabilities
df3 = pd.read_csv(in_fs[3])
# ----+ attach year
df3.loc[:, 'year'] = df['year']
# ----+ drop redundant column
df3.drop('doc_id', axis=1, inplace=True)
# ----+ aggregate around years
df3 = df3.groupby('year').agg(np.mean)

# ----+ dominant topics 
df2 = pd.read_csv(in_fs[2])
# ----+ attach year
df2.loc[:, 'year'] = df['year']
# ----+ drop redundant column
df2.drop('doc_id', axis=1, inplace=True)
# ----+ aggregate around years
gr = df2.groupby(['topic_n', 'year'])
df2 = gr.size().reset_index()
df2.rename({0: 'count'}, axis=1, inplace=True)
df2.loc[:, 'total'] = df2.groupby('year')['count'].transform(np.sum)
df2.loc[:, 'prop'] = df2['count']/df2['total']


# %% slope chart a' la Tufte 

# --+ create figure
fig, ax = plt.subplots(1, 1, figsize=(7.5, 11), sharey=True)
# --+ data series
x = (np.arange(2013, 2020, 1))
y_min, y_max = 0.1, 0.16
# --+ create PANEL A, average pr by year
# --+ plot data
colors= ['tab:blue', 'tab:orange', 'tab:green', 'tab:red', 'tab:purple',
         'tab:gray', 'tab:pink', 'tab:brown']
for i, color in zip(np.arange(0, 8, 1), colors):
    topic = '{}'.format(i)
    y0 = df3.loc[:, topic] 
    ax.plot(x, y0, marker='o', mfc='white', mec='white', ms='5',
            color=color, ls='-', label=topic)
    y1 = df2.loc[df2['topic_n']==i, 'prop']
    for year, j, w in zip(x, y0, y1):
        to_print = '{}'.format(int(w/j*100))
        ax.text(year, j, to_print,
                bbox=dict(boxstyle='circle',
                   ec=('white'),
                   fc=('white'),))
# axes
ax.set_xlabel("Year")
#ax.set_ylabel("")
x_ticks = x 
x_ticklabels = ['{}'.format(i) for i in x_ticks]
y_ticks = np.arange(y_min, y_max + 0.02, 0.02)
y_ticklabels= ['{}\%'.format(int(i * 100)) for i in y_ticks]
ax.set_xticks(x_ticks)
ax.set_xticklabels(x_ticklabels, rotation='vertical')
ax.set_yticks(y_ticks)
ax.set_yticklabels(y_ticklabels)
# reference line
#ax.axvline(x=11, ymin=0, ymax=1, color='r')
# grid
ax.grid(True, ls='--', axis='y', which='major')
# --+ hide all spines while preserving ticks
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)
ax.spines['bottom'].set_visible(False)
ax.spines['left'].set_visible(False)
ax.yaxis.set_ticks_position('right')
ax.xaxis.set_ticks_position('bottom')
# --+ write plot to file
out_f = os.path.join('analysis', 'topicModeling', '.output',
                     'pr_slope_chart.pdf')
plt.savefig(out_f, transparent=True, bbox_inches='tight', pad_inches=0)


# !!!!!!!!!!!!!!!!!!! on going !!!!!!!!!!!!!!!!!!!!!!!!

y_max
