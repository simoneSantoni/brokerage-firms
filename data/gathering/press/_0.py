#!/usr/env/bin python2

"""
Docstring
-------------------------------------------------------------------------------
    _0.py    |    create corpus of text
-------------------------------------------------------------------------------
Author: Simone Santoni, simone.santoni.1@city.ac.uk

Edits:

    - created Sat Apr 13 07:53:16 UTC 2019
    - last change --

Notes: NaN

"""

# %% load libraries
import os
import glob
import pickle
import uuid


# %% set path
#NOTE: change user name if needed
srv = '/home/simon'
prj = 'githubRepos/digital-leadership-center'
fdr = 'sources/press'
wd = os.path.join(srv, prj, fdr)
os.chdir(wd)


# %% function definitions

# get textual data out of .rft
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


# splitting individual articles
def split_string(_bundle):
    '''
    :param : _bundle: sets of factiva items
    :return: None
    :notes : use '### picture' as a tag for splitting text
    '''
    # read file
    with open(_bundle, 'rb') as pipe:
        text_body = pipe.read()
    # split on picture tag
    _articles = text_body.split(b'### picture')[1:]
    # count of articles
    _count = len(_articles)
    # dissect the individual articles
    for i in range(_count):
        focal_article = _articles[i]
        if not b' blogs, ' in focal_article:
            substantive_info = focal_article.split(b'\n\n', 1)[1]
            substantive_info = substantive_info.split(b'\n\n', 2)
            if len(substantive_info) == 3:
                _title = substantive_info[0].strip()
                _attributes = substantive_info[1]
                _text = substantive_info[2]
                parsed = (_title in locals()) & (_attributes in locals())\
                         & (_text is locals())
                if not parsed:
                    # document id
                    document_id = str(uuid.uuid1())
                    # write data
                    out_f = '{}.pickle'.format(document_id)
                    _l = [document_id, _title, _attributes, _text]
                    with open(out_f, 'wb') as pipe:
                       pickle.dump(_l, pipe)

# %% get textual data out of .rtf

# scan for files
os.chdir('.data')
in_files = glob.glob('*.rtf')

# deploy function
for f in in_files:
    get_txt(f)

# remove garbage
images = glob.glob('*.jpg') + glob.glob('*.png')
for image in images:
    os.remove(image)

# reset wd
os.chdir(wd)


# %% split on the string function

# list of txt files to parse
os.chdir('.data')
in_files = glob.glob('*.txt')

# run
for f in in_files:
    split_string(f)

# reset wd
os.chdir(wd)
