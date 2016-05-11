#!/usr/bin/env python
""" Copy unique files to repo/objects

"""

from os import listdir, makedirs, unlink
from os.path import abspath, dirname, join as pjoin, isdir, exists
import shutil
from glob import glob
from argparse import ArgumentParser
from hashlib import sha1

MY_DIR = dirname(__file__)
REPO_DIR = abspath(pjoin(MY_DIR, '..'))
COMMIT_MSG_FNAME = 'message.txt'
DIR_LIST_FNAME = 'directory_listing.txt'


def hash_for(fname):
    with open(fname, 'rb') as fobj:
        contents = fobj.read()
    return sha1(contents).hexdigest()


def hash_move(fname, object_dir):
    hash = hash_for(fname)
    out_fname = pjoin(object_dir, hash)
    shutil.move(fname, out_fname)


def move_snapshot(dir, object_dir):
    for fname in listdir(dir):
        path = pjoin(dir, fname)
        hash_move(path, object_dir)
    shutil.rmtree(dir)


def get_parser():
    parser = ArgumentParser()
    parser.add_argument('root_dir',
                        default=REPO_DIR,
                        nargs='?',
                        help='directory for which to move snapshots')
    return parser


def main():
    """ Show graph for snapshots """
    args = get_parser().parse_args()
    root_dir = args.root_dir
    object_dir = pjoin(root_dir, 'repo', 'objects')
    if not isdir(object_dir):
        makedirs(object_dir)
    # Identify snapshot directories by 'message.txt' files
    globber = pjoin(root_dir, '*', COMMIT_MSG_FNAME)
    for message_fname in glob(globber):
        move_snapshot(dirname(message_fname), object_dir)


if __name__ == '__main__':
    main()
