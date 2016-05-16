""" Test message utilities
"""

import sys
from os.path import join as pjoin, abspath, dirname

MY_PATH = dirname(__file__)
sys.path.append(abspath(pjoin(MY_PATH, '..')))

from nobel_prize import (read_info, write_info, msg2info, info2str)

from nose.tools import assert_equal

MSG1 = pjoin(MY_PATH, 'message1.txt')
MSG2 = pjoin(MY_PATH, 'message2.txt')
MSG8 = pjoin(MY_PATH, 'message8.txt')


def test_round_trip():
    for msg_fname in (MSG1, MSG2, MSG8):
        with open(msg_fname, 'rt') as fobj:
            message = fobj.read()
        info = read_info(msg_fname)
        info_plus = msg2info(message)
        info_plus.update(dict(message=message, path=msg_fname))
        assert_equal(info, info_plus)
        assert_equal(info2str(info), message)
