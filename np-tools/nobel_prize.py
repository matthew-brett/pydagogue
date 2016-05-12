#!/usr/bin/env python
""" Configuration for nobel prize utilities
"""

from os.path import (dirname, join as pjoin, abspath)
import re

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

if __name__ == '__main__':
    print(DEFAULT_PATH)
