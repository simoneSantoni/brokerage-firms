#!/usr/bin/env python3

"""
Docstring
------------------------------------------------------------------------------

------------------------------------------------------------------------------

Author: Simone Santoni, simone.santoni.1@city.ac.uk

Edits:
    - created
    - last edit

Notes: NaN

"""

# %% load libraries
# basic operations
import logging
# load data from mongodb
from pymongo import MongoClient
# data analysis/management/manipulation
import pandas as pd
# nlp pipeline
import spacy
import en_core_web_lg
# building corpus/dictionary
import gensim
from gensim import corpora


# %% check software versions
print("""
spaCy version: {}
Gensim version: {}
""".format(spacy.__version__, gensim.__version__))


# %% read data

# create client
uri = "mongodb://simone:DELL123@10.16.142.91/default_db?authSource=admin"
client = MongoClient(uri)

# pick-up db
db = client.digitalTechs

# load the data
df = pd.DataFrame(list(db.find()))


# %% clean data

# basic cleaning
# -- date as datetime
df.loc[:, 'date'] = pd.to_datetime(df['date.$date'])
# -- get timespans
df.loc[:, 'year'] = df['date'].dt.year
# -- drop column
df.drop(['date.$date', '_id.$oid'], axis=1, inplace=true)
# -- remove returns
df.loc[:, 'text'] = df['text'].str.replace('\n', '')

# arrange data for sequential lda
# -- order data by year of publication
df.sort_values('year', inplace=true)
# -- get stacks by year
data = df.groupby('year').size()
# -- time slices
time_slices = data.values

# prepare list to pass through spacy
docs = [article.strip().lower() for article in df.text]

# hyphen to underscores
docs = [re.sub(r'\b-\b', '_', text) for text in docs]


# %% exploratory data analysis

# barchart of the distribution of articles over time
# -- data series
x = data.index
y = time_slices
# -- labels
x_labels = ['%s' % i for i in x if i < 2019] + ['2019*']
y_labels = ['%s' % i for i in np.arange(0, 1400, 200)]
# -- create figure
plt = plt.figure(figsize=(6, 4))
# -- populate figure with a plot
ax = plt.add_subplot(1, 1, 1)
# -- plot data
ax.bar(x, y, color='r', alpha=0.5)
# -- axis properties
ax.set_xticks(x)
ax.set_xticklabels(x_labels, fontsize=14, rotation='vertical')
ax.set_xlabel('year', fontsize=14)
ax.set_yticklabels(y_labels, fontsize=14)
ax.set_ylabel('counts of documents', fontsize=14)
# -- annotation
notes = """notes: * the 2019 bucket contains documents published
              between jan-01 and mar-31."""
plt.text(0.12, -0.25, notes, fontsize=12)
# -- grid
ax.grid(true, ls='--', axis='y', color='white')
# -- save plot
plt.savefig('barchart.pdf')


# %% NLP pipeline

# load spaCy model 'web_lg'
nlp = en_core_web_lg.load()

# expand on spaCy's stopwords
# -- my stopwrods
my_stopwords = ['\x1c',
                'ft', 'wsj', 'time', 'sec',
                'say', 'says', 'said',
                'mr.', 'mister', 'mr', 'miss', 'ms',
                'inc']
# -- expand on spacy's stopwords
for stopword in my_stopwords:
    nlp.vocab[stopword].is_stop = true

# tokenize text
docs_tokens, tmp_tokens = [], []

for doc in docs:
    tmp_tokens = [token.lemma_ for token in nlp(doc)
                  if not token.is_stop
                  and not token.is_punct
                  and not token.like_num
                  and not token.like_url
                  and not token.like_email
                  and not token.is_currency
                  and not token.is_oov]
    docs_tokens.append(tmp_tokens)
    tmp_tokens = []

# take into account bi- and tri-grams
# -- get rid of common terms
common_terms = [u'of', u'with', u'without', u'and', u'or', u'the', u'a',
                u'not', 'be', u'to', u'this', u'who', u'in']
# -- find phrases as bigrams
bigram = phrases(docs_tokens,
                 min_count=50,
                 threshold=5,
                 max_vocab_size=50000,
                 common_terms=common_terms)
# -- fing phrases as trigrams
trigram = phrases(bigram[docs_tokens],
                  min_count=50,
                  threshold=5,
                  max_vocab_size=50000,
                  common_terms=common_terms)

# uncomment if bi-grammed, tokenized document is preferred
#docs_phrased = [bigram[line] for line in docs_tokens]

# check outcome of nlp pipeline
print('''
=============================================================================
published article: {}

=============================================================================
tokenized article: {}

=============================================================================
tri-grammed tokenized article: {}

'''.format(docs[1],
           docs_tokens[1],
           docs_phrased[1]))


# %% get corpus & dictionary to use for further nlp analysis

# get dictionary and write it to a file
pr_dictionary = dictionary(docs_phrased)
pr_dictionary.save('/tmp/pr_dictionary.dict')

# get corpus and write it to a file
pr_corpus = [pr_dictionary.doc2bow(doc) for doc in docs_phrased]
corpora.SvmLightCorpus.serialize('/tmp/pr_corpus.svmlight', corpus)

