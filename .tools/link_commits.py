#!/usr/bin/env python
""" Link commits with hashes of the messages
"""

from os.path import (dirname, join as pjoin, abspath)

from hashlib import sha1

COMMIT_MSG_FNAME = 'message.txt'

LINKS = (('2', ('1',)),
         ('3', ('2',)),
         ('4', ('3',)),
         ('5', ('4',)),
         ('6', ('5',)),
         ('7', ('6',)),
         ('7_josephine', ('6',)),
         ('8', ('7', '7_josephine')),
        )

MY_PATH = abspath(dirname(__file__))
DIR_PATH = abspath(pjoin(MY_PATH, '..'))

def msg_for(suffix):
    return pjoin(DIR_PATH, 'snapshot_' + suffix, COMMIT_MSG_FNAME)


def read_file(fname):
    with open(fname, 'rb') as fobj:
        contents = fobj.read()
    return contents


def make_links(link_from, link_tos):
    shas = [sha1(read_file(msg_for(lt))).hexdigest()
            for lt in link_tos]
    parents = 'Parents: {}\n'.format(' '.join(shas))
    from_fname = msg_for(link_from)
    from_msg = read_file(from_fname)
    with open(from_fname, 'wt') as fobj:
        fobj.write(from_msg)
        fobj.write(parents)


def main():
    for link_from, link_tos in LINKS:
        make_links(link_from, link_tos)


if __name__ == '__main__':
    main()
