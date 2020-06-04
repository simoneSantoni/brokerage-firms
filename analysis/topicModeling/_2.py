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
%matplotlib inline
plt.style.use('seaborn-bright')
rc('font',**{'family':'serif','serif':['Computer Modern Roman']})
rc('text', usetex=True)
colors= ['tab:blue', 'tab:orange', 'tab:green', 'tab:red', 'tab:purple',
         'tab:gray', 'tab:pink', 'tab:brown']

# %% document attributes

# open monog pipeline
'''
I'm working on machine != dell_1
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
# load the data
df = pd.DataFrame(list(db.press_releases.find()))
# --+ stop server
server.stop()


# %% data to visualize

# manipulate

# --+ time slices
time_slices = [265, 385, 479, 825, 1070, 862, 327]
years = [2013, 2014, 2015, 2016, 2017, 2018, 2019]

df_year = []

for i, j in zip(years, time_slices):
    to_append = np.repeat(i, j)
    df_year = np.hstack([df_year, to_append])


# --+ 8 topic model
# ----+ doc2topic probabilities
in_f = os.path.join('analysis', 'topicModeling', '.output',
                    '8t_doc_topic_pr.csv')
df0 = pd.read_csv(in_f)
# ----+ attach year
df0.loc[:, 'year'] = df_year
# ----+ drop redundant column
df0.drop('doc_id', axis=1, inplace=True)
# ----+ aggregate around years
df0 = df0.groupby('year').agg(np.mean)

# ----+ dominant topics
in_f = os.path.join('analysis', 'topicModeling', '.output',
                    '8t_dominant_topics.csv')
df1 = pd.read_csv(in_f)
# ----+ attach year
df1.loc[:, 'year'] = df_year
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
y_min, y_max = 0.10, 0.20
# --+ create PANEL A, average pr by year
# --+ plot data
for i, color in zip(np.arange(0, 8, 1), colors):
    topic = '{}'.format(i)
    y0 = df0.loc[:, topic] 
    ax1.plot(x, y0, marker='o', mfc=color, mec=color, ms='4',
            color=color, ls='-', label=topic)
    #y1 = df1.loc[df1['topic_n']==i, 'prop']
    #for year, j, w in zip(x, y0, y1):
    #    to_print = '{}'.format(int(w*100))
    #    ax1.text(year, j, to_print,
    #            bbox=dict(boxstyle='circle',
    #                      ec=('white'),
    #                      fc=('white'),))
# --+ axes
ax1.set_xlabel("Year")
#ax1.set_ylabel("")
x_ticks = x 
x_ticklabels = ['{}'.format(i) for i in x_ticks]
y_ticks = np.arange(y_min, y_max+0.05, 0.05)
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
y = df0.loc[2013].values
y[3] = y[7] + 0.01
y[5] = y[7] - 0.01
topic_labels =[
    'Topic 1: company;\nventure; start-up;\n technology; include',
    'Topic 2: fund;\ninvestment; asset;\nmarket; investor',
    'Topic 3: market;\nrate; growth;\n price; rise',
    'Topic 4: loan;\ncredit; insurance;\npay; accord',
    'Topic 5: fund;\nfirm; capital;\ninvestment; price',
    'Topic 6: bank;\n financial; rule;\nregulator; firm',
    'Topic 7: datum;\ntechnology; people;\ncustomer; work\nservice',
    'Topic 8: company;\ngroup; China; deal;\nproperty'
]
for i, color in zip(np.arange(0, 8,1), colors):
    topic = '{}'.format(i)
    y_pos = y[i]
    to_print = topic_labels[i]
    x_pos = 0.1
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
                     'pr_slope_chart.pdf')
plt.savefig(out_f, transparent=True, bbox_inches='tight', pad_inches=0)


# %% topology of topics

# doc2topic probabilities
# --+ load 
in_f = os.path.join('analysis', 'topicModeling', '.output',
                    '8t_doc_topic_pr.csv')
df0 = pd.read_csv(in_f)
# --+ attach year
df0.loc[:, 'year'] = df_year
# --+ get rid of missing values
df0.fillna(0, inplace=True)
# --+ get correlations among topics
correlations = []
for year in years:
    for i in np.arange(0, 8, 1):
        for j in np.arange(0, 8, 1):
            if i < j:
                x = df0.loc[df0['year'] == year, '%s' % i]
                y = df0.loc[df0['year'] == year, '%s' % j]
                r, p = pearsonr(x, y)
                to_append = [i, j, r, p, year]
                correlations.append(to_append)
# --+ edges along with weights
edges = pd.DataFrame(correlations, columns=['u', 'v', 'r', 'p', 'year'])
# --+ node attributes
df0.drop('doc_id', axis=1, inplace=True)
node_attrs = df0.groupby('year').aggregate(np.mean)
# node labels
topic_set = np.arange(0, 8, 1)
labels = dict(zip(topic_set,
                  ['{}'.format(i + 1) for i in topic_set]))
# ----+ fix the color of edges
ts_min = np.min(edges.r)
ts_max = np.max(edges.r)


# --+ itearate over years

year = 2013

g = nx.from_pandas_edgelist(df=edges.loc[edges['year'] == year],
                            source='u', target='v',
                            edge_attr=['strength', 'year'],
                            create_using=nx.MultiGraph)

# ----+ add node attributes
n_size = node_attrs.loc[2013].values

# ----+ add edge attributes
ts_dict = nx.get_edge_attributes(g, 'strength')
ts = [ts_dict[d] for d in ts_dict]

# ----+ create figure
fig = plt.figure(figsize=(4, 4))
# ----+ positions
pos = nx.circular_layout(g)
# ----+ draw networks
nx.draw_networkx_nodes(g, pos, node_color=colors, node_size=300)
nx.draw_networkx_edges(g, pos, linewidths=ts)
nx.draw_networkx_labels(g, pos, labels=labels, font_color='white')
# ----+ axis off
plt.axis('off')
# ----+ write plot to file
out_f = os.path.join('analysis', 'topicModeling', '.output',
                     'pr_topic_topology.pdf')
plt.savefig(out_f, bbox_inches='tight', pad_inches=0, transparent=True)
