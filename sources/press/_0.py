#!/usr/env/bin python2

"""
DOCSTRING
-------------------------------------------------------------------------------
                       CREATE CORPUS OF TEXT
-------------------------------------------------------------------------------
Author: Simone Santoni, simone.santoni.1@city.ac.uk

Dates:
    - created Sat Apr 13 07:53:16 UTC 2019
    - revise --
"""

# %% load libraries
import os
import glob
import pickle
import uuid


# %% set path
srv = '/home/simone'
prj = 'githubRepos/digital-leadership-center'
fdr = 'sources/press'
wd = os.path.join(srv, prj, fdr)
os.chdir(wd)


# %% scan for files
in_files = glob.glob(os.path.join('.data', '*.rtf'))


# %% get textual data out of .rft

# define custom function
def get_txt(_bundle):
    '''
    argument: bundle of .rtf files
    return  : None
    notes   : `unrtf' required
    '''
    # compose command
    _software = 'unrtf'
    _in = _bundle
    _option = '--text'
    _to = '>'
    _out = _bundle.strip('rtf') + 'txt'
    _cmd = ' '.join([_software, _in, _option, _to, _out])
    # run command
    os.system(_cmd)


# deploy function
for f in in_files:
    get_txt(f)


# remove garbage
images = glob.glob('*.jpg') + glob.glob('*.png')

for image in images:
    os.remove(image)


# %% split on the string function

'''
use '### picture' as a tag for splitting text
'''

# get list of txt files to parse
bundles = glob.glob('*.txt')


def split_string(_bundle):
    '''
    :param _bundle: sets of factiva items
    :return:
    '''

    # read file
    with open(_bundle, 'rb') as pipe:
        text_body = pipe.read()

    # split on picture tag
    _articles = text_body.split('### picture')[1:]

    # count of articles
    _count = len(_articles)

    # dissect the individual articles
    for i in range(_count):
        focal_article = _articles[i]

        if not ' blogs, ' in focal_article:
            substantive_info = focal_article.split('\n\n', 1)[1]
            substantive_info = substantive_info.split('\n\n', 2)

            if len(substantive_info) == 3:
                _title = substantive_info[0].strip()
                _attributes = substantive_info[1]
                _text = substantive_info[2]

                parsed = (_title in locals()) & (_attributes in locals())\
                         & (_text is locals())

                #in_scope = ('2017' in _attributes) | ('2018' in _attributes)

                if not parsed:

                    # document id
                    document_id = str(uuid.uuid1())

                    # write data
                    _srv = srv
                    _path = 'dropbox/dataprojects/code/ai/pressrelease/factiva'
                    _folder = 'b11148e2-98f7-11e9-92d0-8c859092e3b0'
                    _file = document_id + '.pickle'
                    _out = os.path.join(_srv, _path, _folder, _file)
                    _l = [document_id, _title, _attributes, _text]

                   with open(_out, 'wb') as pipe:
                       pickle.dump(_l, pipe)


# %% deploy parsing function

for bundle in bundles:
    split_string(bundle)
