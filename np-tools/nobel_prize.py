#!/usr/bin/env python
""" Configuration and utilities for nobel prize scripts
"""

from os.path import (dirname, join as pjoin, abspath)
import re
from hashlib import sha1

MY_PATH = abspath(dirname(__file__))
DEFAULT_PATH = abspath(pjoin(MY_PATH, '..', 'working', 'nobel_prize'))

# Name of the commit message file, used for retrieving commit date
COMMIT_MSG_FNAME = 'message.txt'

# Format of date recorded in commit message file
DATE_FMT = 'Date: %B %d %Y, %H.%M'

# Regular expression identifying snapshot directory
SNAPSHOT_RE = re.compile(r'snapshot_(\d+)')

# Filename for directory listing
DIR_LIST_FNAME = 'directory_listing.txt'


def hash_for(fname):
    with open(fname, 'rb') as fobj:
        contents = fobj.read()
    return sha1(contents).hexdigest()


def msg2info(message):
    msg_info = {'parents': []}
    for line in message.splitlines():
        key, value = line.strip().split(': ', 1)
        key = key.lower()
        if key == 'parents':
            value = value.split()
        msg_info[key] = value
    return msg_info


def read_info(message_fname):
    with open(message_fname, 'rt') as fobj:
        message = fobj.read()
    info = msg2info(message)
    info['path'] = message_fname
    info['message'] = message
    return info


def info2str(info):
    out = """\
Date: {date}
Author: {author}
Notes: {notes}
""".format(**info)
    if info['parents']:
        out += 'Parents: {}\n'.format(' '.join(info['parents']))
    return out


def write_info(info):
    with open(info['path'], 'wt') as fobj:
        fobj.write(info2str(info))


if __name__ == '__main__':
    print(DEFAULT_PATH)
