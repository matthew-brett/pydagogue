#!/usr/bin/env python
""" Link commits with hashes of the messages
"""

import sys
from os.path import (dirname, join as pjoin, abspath)
from glob import glob
from hashlib import sha1
from argparse import ArgumentParser

MY_PATH = dirname(__file__)
sys.path.append(abspath(MY_PATH))
from nobel_prize import (DEFAULT_PATH, COMMIT_MSG_FNAME, DIR_LIST_FNAME,
                        hash_for, read_info, info2str, write_info)


def read_expand_info(message_fname):
    info = read_info(message_fname)
    info['old_hash'] = sha1(info['message']).hexdigest()
    dir_list_path = pjoin(dirname(message_fname), DIR_LIST_FNAME)
    info['directory hash'] = hash_for(dir_list_path)
    if 'parents' in info:
        info['fixed_parents'] = [False] * len(info['parents'])
    else:
        info['fixed_parents'] = []
    return info


def find_roots(infos):
    return [i for i in infos if all(i['fixed_parents'])]


def fix_from(root, infos):
    """ Add tree hash; fix parents """
    # Assume root has correct parents (or none)
    old_hash = root['old_hash']
    new_hash = sha1(info2str(root)).hexdigest()
    for info in infos:
        if not 'parents' in info:
            continue
        if old_hash in info['parents']:
            index = info['parents'].index(old_hash)
            info['parents'][index] = new_hash
            info['fixed_parents'][index] = True


def get_parser():
    parser = ArgumentParser()
    parser.add_argument('root_dir',
                        default=DEFAULT_PATH,
                        nargs='?',
                        help='directory in which to add tree hashes')
    return parser


def main():
    """ Process graph in very dumb way """
    args = get_parser().parse_args()
    root_dir = args.root_dir
    # Identify snapshot directories by 'message.txt' files
    globber = pjoin(root_dir, '*', COMMIT_MSG_FNAME)
    infos = []
    for message_fname in glob(globber):
        infos.append(read_expand_info(message_fname))
    processed_roots = []
    while True:
        current_roots = find_roots(infos)
        new_roots = [r for r in current_roots if r not in processed_roots]
        if len(new_roots) == 0:
            break
        for root in new_roots:
            fix_from(root, infos)
        processed_roots += new_roots
    for info in infos:
        write_info(info)


if __name__ == '__main__':
    main()
