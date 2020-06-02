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
# --+ 8 topics, doc2topic pr
df3 = pd.read_csv(in_fs[3])
# --+ attach year
df3.loc[:, 'year'] = df['year']
# --+ drop redundant column
df3.drop('doc_id', axis=1, inplace=True)
# --+ aggregate around years
df3 = df3.groupby('year').agg(np.mean)

# %% slope chart a' la Tufte 

# --+ create figure
fig, [ax0, ax1] = plt.subplots(1, 2, figsize=(6, 4), sharey=True)
# --+ data series
x = (np.arange(2013, 2020, 1))
# --+ create PANEL A, average pr by year
# --+ plot data
for i in np.arange(0, 8, 1):
    topic = '{}'.format(i)
    y = df3.loc[:, topic]
    ax0.plot(x, y, marker='o', color='k', ls='', label=topic)
# axes
ax0.set_xlabel("Year")
#ax0.set_ylabel("")
x_ticks = x 
x_labels = ['{}'.format(i) for i in x_ticks]
ax0.set_xticks(x_ticks)
ax0.set_xticklabels(x_labels, rotate)
# reference line
#ax0.ax0vline(x=11, ymin=0, ymax0=1, color='r')
# grid
ax0.grid(True, ls='--', axis='y', which='major')
# --+ hide all spines while preserving ticks
ax0.spines['right'].set_visible(False)
ax0.spines['top'].set_visible(False)
ax0.spines['bottom'].set_visible(False)
ax0.spines['left'].set_visible(False)
ax0.yaxis.set_ticks_position('left')
ax0.xaxis.set_ticks_position('bottom')
ax0.yaxis.set_ticks_position('left')
ax0.xaxis.set_ticks_position('bottom')
# -- textbox
ax0.text(0, 1, u'$A$', fontsize=13)
# --+ PANEL B
# --+ plot data
#ax1.plot(x1, y1, marker='o', color='k', ls='')
## axes
#ax1.set_xlabel("Number of topics retained")
#ax1.set_xticks(np.arange(10, 35, 5))
## grid
#ax1.grid(True, ls='--', axis='y', which='major')
## --+ hide all spines while preserving ticks
#ax1.spines['right'].set_visible(False)
#ax1.spines['top'].set_visible(False)
#ax1.spines['bottom'].set_visible(False)
#ax1.spines['left'].set_visible(False)
##ax1.yaxis.set_ticks_position('left')
##ax1.xaxis.set_ticks_position('bottom')
##ax1.yaxis.set_ticks_position('left')
##ax1.xaxis.set_ticks_position('bottom')
## --+ textbox
#ax0.text(10, 0.51, u'$B$', fontsize=13)
# --+ write plot to file
out_f = os.path.join('analysis', 'topicModeling', '.output',
                     'pr_slope_chart.pdf')
plt.savefig(out_f)

,
            transparent=True,
            bbox_inches='tight',
            pad_inches=0)


# !!!!!!!!!!!!!!!!!!! on going !!!!!!!!!!!!!!!!!!!!!!!!
df3.head()

