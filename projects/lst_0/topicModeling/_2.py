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
srv = '/Users/simone'
prj = 'githubRepos/digital-leadership-center'
wd = os.path.join(srv, prj)
os.chdir(wd)


# %% viz options
#%matplotlib inline
plt.style.use('seaborn-bright')
rc('font',**{'family':'serif','serif':['Computer Modern Roman']})
rc('text', usetex=True)
colors= ['tab:blue', 'tab:orange', 'tab:green', 'tab:red', 'tab:purple',
         'tab:gray', 'tab:pink', 'tab:brown']


# %% document attributes

# open mono pipeline
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
#server.stop()


# %% data to visualize

# manipulate

# --+ time slices
time_slices = [265, 385, 479, 825, 1070, 862, 713]
years = [2013, 2014, 2015, 2016, 2017, 2018, 2019]

df_year = []

for i, j in zip(years, time_slices):
    to_append = np.repeat(i, j)
    df_year = np.hstack([df_year, to_append])


# --+ 8 topic model
# ----+ doc2topic probabilities
in_f = os.path.join('scripts', 'analysis', 'topicModeling', '.output',
                    '8t_doc_topic_pr.csv')
df0 = pd.read_csv(in_f)
# ----+ attach year
df0.loc[:, 'year'] = df_year
# ----+ drop redundant column
df0.drop('doc_id', axis=1, inplace=True)
# ----+ aggregate around years
df0 = df0.groupby('year').agg(np.mean)

# ----+ dominant topics
in_f = os.path.join('scripts', 'analysis', 'topicModeling', '.output',
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
# --+ partition the figure into 2 subplots with 'gridspec'
gs = gridspec.GridSpec(1, 2,
                       figure=fig, 
                       hspace=0, wspace=0, 
                       width_ratios=[1, 4])
# add plots
ax1 = fig.add_subplot(gs[0, 1]) 
ax0 = fig.add_subplot(gs[0, 0], sharey=ax1) 
# --+ data series
x = (np.arange(2013, 2020, 1))
y_min, y_max = 0.10, 0.16
# --+ create PANEL A, average pr by year
# --+ plot data
for i, color in zip(np.arange(0, 8, 1), colors):
    topic = '{}'.format(i)
    y0 = df0.loc[:, topic] 
    ax1.plot(x, y0, marker='o', mfc=color, mec=color, ms='4',
            color=color, ls='-', label=topic)
# --+ axes
ax1.set_xlabel("Year")
#ax1.set_ylabel("")
x_ticks = x 
x_ticklabels = ['{}'.format(i) for i in x_ticks]
y_ticks = np.arange(y_min, y_max+0.01, 0.02)
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
y[6] = y[3] - 0.004
y[2] = y[0] - 0.003
y[4] = y[0] + 0.004
topic_labels =[
    'Topic 1: people;\ncredit; loan;\n risk; pay',
    'Topic 2: market;\nrate; growth;\n price; rise',
    'Topic 3: bank;\n financial; rule;\nregulator; firm',
    'Topic 4: datum;\ntechnology; people;\ncustomer; work\nservice',
    'Topic 5: business;\nback; chief;\nexecutive; group',
    'Topic 6: fund;\ninvestor; price;\nmanager; assett',
    'Topic 7: company;\nventure; start-up;\ninvestor; technology',
    'Topic 8: firm;\ncapital; partner;\naccord; equity'
]

for i, color in zip(np.arange(0, 8, 1), colors):
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
out_f = os.path.join('scripts', 'analysis', 'topicModeling', '.output',
                     'pr_slope_chart.pdf')
#plt.show()
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

# --+ create figure
fig = plt.figure(figsize=(7.5, 11))
# --+ parition the figure into 2 subplots with 'gridspec'
gs = gridspec.GridSpec(4, 4,
                       figure=fig, 
                       hspace=0, wspace=0)
# --+ add plots
ax0 = fig.add_subplot(gs[0, 0:2]) 
ax1 = fig.add_subplot(gs[0, 2:4])
ax2 = fig.add_subplot(gs[1, 0:2])
ax3 = fig.add_subplot(gs[1, 2:4])
ax4 = fig.add_subplot(gs[2, 0:2])
ax5 = fig.add_subplot(gs[2, 2:4])
ax6 = fig.add_subplot(gs[3, 1:3])
# --+ iterater over years
for year, ax in zip(years, [ax0, ax1, ax2, ax3, ax4, ax5, ax6]):
    g = nx.from_pandas_edgelist(df=edges.loc[edges['year'] == year],
                                source='u', target='v',
                                edge_attr=['r', 'p', 'year'],
                                create_using=nx.Graph)
    # --+ add node attributes
    n_size = node_attrs.loc[2013].values
    # --+ add edge attributes
    # ----+ r, p
    r_dict = nx.get_edge_attributes(g, 'r')
    r = [r_dict[d] for d in r_dict]
    p_dict = nx.get_edge_attributes(g, 'p')
    p = [p_dict[d] for d in p_dict]
    # ----+ code edge style
    e_color, e_style = [], []
    for i, j in zip(p, r):
        if year <= 2017:
            if i > 0.001:
                e_color.append('white'), e_style.append('solid')
            else:
                e_color.append('tab:gray')
                if j > 0:
                    e_style.append('solid')
                else:
                    e_style.append('dotted')
        else:
            if year > 2017:
                if i > 0.05:
                    e_color.append('white'), e_style.append('solid')
                else:
                    e_color.append('tab:gray')
                    if j > 0:
                        e_style.append('solid')
                    else:
                        e_style.append('dotted')
    # --+ positions
    pos = nx.circular_layout(g)
    # --+ draw networks
    nx.draw_networkx_nodes(g, pos, node_color='white', node_size=300, ax=ax)
    # --+ iterate over edges
    e = [d for d in g.edges]
    for d, c, s in zip(e, e_color, e_style):
        if c != 'white':
            nx.draw_networkx_edges(g, pos, edgelist=[d], edge_color=c, style=s,
                                   width=0.75, ax=ax)
        else:
            pass
    # --+ draw labels
    nx.draw_networkx_labels(g, pos, labels=labels, font_color='k', ax=ax)
    # --+ textbox
    ax.text(-1.05, 0.975, year, color='white',
            bbox=dict(boxstyle='round',
                      ec=('white'),
                      fc=('tab:gray')))
    # --+ axis off
    ax.axis('off')
# --+ write plot to file
out_f = os.path.join('analysis', 'topicModeling', '.output',
                     'pr_topic_topology.pdf')
plt.savefig(out_f, bbox_inches='tight', pad_inches=0, transparent=True)


# %% sentiment scores at the topic level

import spacy
import en_core_web_lg
nlp = en_core_web_lg.load()


t1 = ['people', 'credit', 'loan', 'risk', 'pay']
t2 = ['market', 'rate', 'growth', 'price', 'rise']
t3 = ['bank', 'financial', 'rule', 'regulator', 'firm']
t4 = ['datum', 'technology', 'people', 'customer', 'work', 'service']
t5 = ['business', 'back', 'chief', 'executive', 'group']
t6 = ['fund', 'investor', 'price', 'manager', 'assett']
t7 = ['company', 'venture', 'start-up', 'investor', 'technology']
t8 = ['firm', 'capital', 'partner', 'accord', 'equity']

for word in t1:
    doc = nlp(word)
    for token in doc:
        print(token)
