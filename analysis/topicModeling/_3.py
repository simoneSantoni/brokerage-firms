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
from urllib.parse import quote_plus
from sshtunnel import SSHTunnelForwarder
from pymongo import MongoClient
import numpy as np
from scipy.stats import pearsonr
import matplotlib.pyplot as plt
from matplotlib.pyplot import rc
import matplotlib.colors as mcolors
import matplotlib.gridspec as gridspec
import pandas as pd
import networkx as nx
from networkx.algorithms import bipartite


# %% set working dir
srv = '/home/simone'
prj = 'githubRepos/digital-leadership-center'
wd = os.path.join(srv, prj)
os.chdir(wd)


# %% viz options
plt.style.use('seaborn-bright')
rc('font',**{'family':'serif','serif':['Computer Modern Roman']})
rc('text', usetex=True)
colors= ['tab:blue', 'tab:orange', 'tab:green', 'tab:red', 'tab:purple',
         'tab:gray', 'tab:pink', 'tab:brown']

# %% document attributes

# open mongo pipeline
'''
mongo is runnining on a server
'''
# --+ params
mongo_host = "10.16.142.91"
mongo_db = "digitalTechs"
mongo_user = "simone"
mongo_pass = my_pwd # stored within ipython
# --+ server
server = SSHTunnelForwarder(
    mongo_host,
    ssh_username=mongo_user,
    ssh_password=mongo_pass,
    remote_bind_address=('127.0.0.1', 27017)
)
# --+ start server
server.start()
# --+ create client
client = MongoClient('127.0.0.1', server.local_bind_port)
# --+ target db
db = client[mongo_db]
# --+ company-year
df0 = pd.DataFrame(list(db.web_contents_id.find()))
# --+ id 
df1 = pd.DataFrame(list(db.web_tokenized_5_50k.find()))
# --+ stop server
server.stop()

# --+ merge
df1.loc[:, 'doc_id'] = np.arange(0, len(df1), 1)
df = pd.merge(df0, df1, on='_id', how='right')


# %% data to visualize

# load 9 topic model
# --+ doc2topic probabilities
in_f = os.path.join('analysis', 'topicModeling', '.output',
                    '9t_doc_topic_pr.csv')
df2 = pd.read_csv(in_f)

# match year
df = pd.merge(df2, df, on='doc_id', how='inner')
# --+ drop redundant column
df.drop('_id', axis=1, inplace=True)
# --+ remove NaN
df.fillna(0, inplace=True)

# aggregate data around years
df0 = df.groupby('year').agg(np.mean)
# --+ remove redundant col
df0.drop('doc_id', axis=1, inplace=True)

# dominant topics
in_f = os.path.join('analysis', 'topicModeling', '.output',
                    '9t_dominant_topics.csv')
df1 = pd.read_csv(in_f)
# --+ attach year
df1.loc[:, 'year'] = df['year']
# --+ attach entity
df1.loc[:, 'entity'] = df['entity']
# --+ drop redundant column
df1.drop('doc_id', axis=1, inplace=True)

# --+ aggregate around years
gr = df1.groupby(['topic_n', 'year'])
df1 = gr.size().reset_index()
df1.rename({0: 'count'}, axis=1, inplace=True)
df1.loc[:, 'total'] = df1.groupby('year')['count'].transform(np.sum)
df1.loc[:, 'prop'] = df1['count']/df1['total']

# --+ remove 2020 datapoints
df0.drop('2020', axis=0, inplace=True)

# --+ remove topic # 0
df0.drop('0', axis=1, inplace=True)

# ----+ rescale
df0.loc[:, 'tot'] = df0.sum(axis=1)
for i in np.arange(1, 9, 1):
    column = '{}'.format(i)
    df0.loc[:, column] = df0[column] / df0['tot']
# ----+ drop redundant column
df0.drop('tot', axis=1, inplace=True)

# %% slope chart a' la Tufte 

# --+ create figure
fig = plt.figure(figsize=(7.5, 11))
# --+ parition the figure into 2 subplots with 'gridspec'
gs = gridspec.GridSpec(1, 2,
                       figure=fig, 
                       hspace=0, wspace=0, 
                       width_ratios=[1, 4])
# add plots
ax1 = fig.add_subplot(gs[0, 1]) 
ax0 = fig.add_subplot(gs[0, 0], sharey=ax1) 
# --+ data series
x = (np.arange(2013, 2020, 1))
y_min, y_max = 0.07, 0.20
# --+ create PANEL A, average pr by year
# --+ plot data
for i, color in zip(np.arange(1, 9, 1), colors):
    topic = '{}'.format(i)
    y0 = df0.loc[:, topic] 
    ax1.plot(x, y0, marker='o', mfc=color, mec=color, ms='4',
            color=color, ls='-', label=topic)
# --+ axes
ax1.set_xlabel("Year")
#ax1.set_ylabel("")
x_ticks = x 
x_ticklabels = ['{}'.format(i) for i in x_ticks]
y_ticks = np.arange(0.10, y_max+0.05, 0.05)
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
y = [0.155, 0.112, 0.165, 0.09, 0.121, 0.10, 0.185, 0.078]
topic_labels =[
    'Topic 1: job;\nmanagement;\nbusiness;\n university; director',
    'Topic 2: market;\ntrade; fund;\ninvestment; stock',
    'Topic 3: year; video;\nnews; post; day',
    'Topic 4: service;\nproduct; energy;\nnews; technology',
    'Topic 5: bank;\ninsurance; risk;\nfinancial; business',
    'Topic 6: learn;\n science; model;\nresearch; health',
    'Topic 7: datum;\ntechnology;\nanalytics;\nbusiness; legal',
    'Topic 8: azure;\ncloud; datum;\nservice; app'
]
for i, color in zip(np.arange(1, 9, 1), colors):
    topic = '{}'.format(i)
    y_pos = y[i - 1]
    to_print = topic_labels[i - 1]
    x_pos = 0
    ax0.text(x_pos, y_pos, to_print, color=color, verticalalignment='center',
             bbox=dict(boxstyle='round',
                       ec=('white'),
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
                     'ws_slope_chart.pdf')
plt.savefig(out_f, transparent=True, bbox_inches='tight', pad_inches=0)


# %% arrange data to pass to R

# get the most prominent topic by company-year
# --+ group data
gr = df1.groupby(['entity', 'year', 'topic_n'], as_index=False)
# --+ remove uninteresting topic
df1 = df1.loc[df1['topic_n'] != 0]

# --+ get collapsd df
df2 = pd.DataFrame(gr.size())
# --+ some cleaning
# ----+ reset index
df2.reset_index(inplace=True)
# ----+ rename cols
df2.rename(columns={0: 'count'}, inplace=True)
# --+ get most recurrent topic
gr = df2.groupby(['entity', 'year'])
df2.loc[:, 'max'] = gr['count'].transform(np.max)

# --+ slice data
df3 = df2.loc[df2['count'] == df2['max']]
df3 = df3[df3['year'] != 2020]

# ----+ take first
gr = df3.groupby(['entity', 'year'])
df3.loc[:, 'take_first'] = 1
df3.loc[:, 'take_first'] = gr['take_first'].transform(np.cumsum)
df3 = df3.loc[df3['take_first'] == 1]

# --+ reshape data
df3 = pd.pivot_table(df3, index='entity', columns='year', values='topic_n')

# --+ remove companies with NaNs
df3.dropna(inplace=True)

# --+ write plot to file
out_f = os.path.join('analysis', 'topicModeling', '.output',
                     'ws_seq_analysis.csv')
df3.to_csv(out_f, index=False)

# get topic entropy within company-year
# --+ get total instances
df2.loc[:, 'tot'] = gr['count'].transform(np.sum)
# --+ get proportions
df2.loc[:, 'prop_2'] = np.square(df2['count']/df2['tot'])
# --+ collapse data
df4 = pd.DataFrame(gr['prop_2'].agg(np.sum))
df4.reset_index(inplace=True)
df4.loc[:, 'bi'] = 1 - df4['prop_2']
# --+ write plot to file
out_f = os.path.join('analysis', 'topicModeling', '.output',
                     'ws_ts_clustering.csv')
df4.to_csv(out_f, index=False)

