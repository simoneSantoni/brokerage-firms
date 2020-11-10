# !/usr/env/bin python3

"""
Docstring

------------------------------------------------------------------------------

------------------------------------------------------------------------------

Author: Simone Santoni, simone.santoni.1@city.ac.uk

Edits:

    - created
    - last change


Notes: None.

"""


# %% load libraries

import os
import pandas as pd
from pymongo import MongoClient


# %% setup

srv = '/home/simone'
prj = 'githubRepos/digital-leadership-center'
fdr = 'dataCollection'
cd = os.path.join(srv, prj, fdr)

os.chdir(cd)


# %% load data

# read
df = pd.read_excel(os.path.join('companies', 'bloomberg_export.xlsx'),
                   sheet_name='Results')

# some cleaning
# -- drop redundant column
df.drop(columns=['Unnamed: 0'], axis=1, inplace=True)
# -- rename columns
old_names = df.columns
new_names = ['company', 'postcode', 'nu', 'main_sic', 'latest_account',
             'revenues', 'employees']
df.rename(columns=dict(zip(old_names, new_names)), inplace=True)

# -- revenues to number
df.loc[:, 'revenues'] = pd.to_numeric(df['revenues'], errors='coerce')
# -- sort
df.sort_values(by='revenues', ascending=[False], inplace=True)


# %% write data to mongo

# open pipeline
client = MongoClient()

# pick-up collection
db = client.digitalTechs

# bulk insert
db.companies.insert_many(df.to_dict('records'))

