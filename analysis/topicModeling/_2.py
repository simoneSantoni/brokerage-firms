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
from matplotlib.pyplot import rc
import matplotlib.colors as mcolors
import matplotlib.gridspec as gridspec
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

# manipulate

# --+ 8 topic model
# ----+ doc2topic probabilities
in_f = os.path.join('analysis', 'topicModeling', '.output',
                    '8t_doc_topic_pr.csv')
df0 = pd.read_csv(in_f)
# ----+ attach year
df0.loc[:, 'year'] = df['year']
# ----+ drop redundant column
df0.drop('doc_id', axis=1, inplace=True)
# ----+ aggregate around years
df0 = df0.groupby('year').agg(np.mean)

# ----+ dominant topics
in_f = os.path.join('analysis', 'topicModeling', '.output',
                    '8t_dominant_topics.csv')
df1 = pd.read_csv(in_f)
# ----+ attach year
df1.loc[:, 'year'] = df['year']
# ----+ drop redundant column
df1.drop('doc_id', axis=1, inplace=True)
# ----+ aggregate around years
gr = df1.groupby(['topic_n', 'year'])
df1 = gr.size().reset_index()
df1.rename({0: 'count'}, axis=1, inplace=True)
df1.loc[:, 'total'] = df1.groupby('year')['count'].transform(np.sum)
df1.loc[:, 'prop'] = df1['count']/df1['total']


# %% slope chart a' la Tufte 

# --+ create figure
fig = plt.figure(figsize=(7.5, 11))
# --+ parition the figure into 4 subplots with 'gridspec'
gs = gridspec.GridSpec(1, 2, # we want 2 rows, 2 cols
                       figure=fig, # this gs applies to figure
                       hspace=0, wspace=0, # separation between plots
                       width_ratios=[1, 4]) # ratio between the first ans second row
# add plots
ax1 = fig.add_subplot(gs[0, 1]) # and so on and so forth...
ax0 = fig.add_subplot(gs[0, 0], sharey=ax1) # this will occupy the first row-first colum
# --+ data series
x = (np.arange(2013, 2020, 1))
y_min, y_max = 0.1, 0.16
# --+ create PANEL A, average pr by year
# --+ plot data
colors= ['tab:blue', 'tab:orange', 'tab:green', 'tab:red', 'tab:purple',
         'tab:gray', 'tab:pink', 'tab:brown']
for i, color in zip(np.arange(0, 8, 1), colors):
    topic = '{}'.format(i)
    y0 = df0.loc[:, topic] 
    ax1.plot(x, y0, marker='o', mfc='white', mec='white', ms='3',
            color=color, ls='-', label=topic)
    y1 = df1.loc[df1['topic_n']==i, 'prop']
    for year, j, w in zip(x, y0, y1):
        to_print = '{}'.format(int(w*100))
        ax1.text(year, j, to_print,
                bbox=dict(boxstyle='circle',
                          ec=('white'),
                          fc=('white'),))
# --+ axes
ax1.set_xlabel("Year")
#ax1.set_ylabel("")
x_ticks = x 
x_ticklabels = ['{}'.format(i) for i in x_ticks]
y_ticks = np.arange(y_min, y_max + 0.02, 0.02)
y_ticklabels= ['{}\%'.format(int(i * 100)) for i in y_ticks]
ax1.set_xticks(x_ticks)
ax1.set_xticklabels(x_ticklabels, rotation='vertical')
ax1.set_yticks(y_ticks)
ax1.set_yticklabels(y_ticklabels)
# reference line
#ax1.ax1vline(x=11, ymin=0, ymax1=1, color='r')
# --+ grid
ax1.grid(True, ls='--', axis='y', which='major')
# --+ hide all spines while preserving ticks
ax1.spines['right'].set_visible(False)
ax1.spines['top'].set_visible(False)
ax1.spines['bottom'].set_visible(False)
ax1.spines['left'].set_visible(False)
ax1.yaxis.set_ticks_position('right')
ax1.xaxis.set_ticks_position('bottom')
# --+ topic labels
y = [.1255, .1205, .1305, .112, .10975, .1185, .165, .1165]
for i, color in zip(np.arange(0, 8,1), colors):
    topic = '{}'.format(i)
    y_pos = y[i]
    to_print = 'Topic {}'.format(i + 1)
    x_pos = 0.3
    ax0.text(x_pos, y_pos, to_print, color=color,
             bbox=dict(boxstyle='round',
                       ec=(color),
                       fc=('white'),))
#ax1.set_ylabel("")
x_ticks = [-.5, 0, +.5] 
x_ticklabels = []
y_ticks = y_ticks
y_ticklabels= []
ax0.set_xticks([])
ax0.set_xticklabels(x_ticklabels)
# --+ hide all spines while preserving ticks
ax0.spines['right'].set_visible(False)
ax0.spines['top'].set_visible(False)
ax0.spines['bottom'].set_visible(False)
ax0.spines['left'].set_visible(False)
ax0.axis('off') #.set_ticks_position('right')
#ax0.xaxis.set_ticks_position('bottom')
# --+ write plot to file
out_f = os.path.join('analysis', 'topicModeling', '.output',
                     'pr_slope_chart.pdf')
plt.savefig(out_f, transparent=True, bbox_inches='tight', pad_inches=0)


# !!!!!!!!!!!!!!!!!!! on going !!!!!!!!!!!!!!!!!!!!!!!!
df3.loc[2013]


