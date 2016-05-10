""" Configuration for nobel prize utilities
"""

from os.path import (dirname, join as pjoin, abspath)
import re
from locale import getpreferredencoding

MY_PATH = abspath(dirname(__file__))
DEFAULT_PATH = abspath(pjoin(MY_PATH, '..', 'working', 'nobel_prize'))
ENCODING = getpreferredencoding()

# Name of the commit message file, used for retrieving commit date
COMMIT_MSG_FNAME = 'message.txt'

# Format of date recorded in commit message file
DATE_FMT = 'Date: %B %d %Y, %H.%M'

# Regular expression identifying snapshot directory
SNAPSHOT_RE = re.compile(r'snapshot_(\d+)')
