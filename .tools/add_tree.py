#!/usr/bin/env python
""" Link commits with hashes of the messages
"""

from os.path import (dirname, join as pjoin, abspath, isdir, isfile, basename)
from glob import glob
from collections import OrderedDict
from hashlib import sha1
from argparse import ArgumentParser

MY_DIR = dirname(__file__)
REPO_DIR = abspath(pjoin(MY_DIR, '..'))
COMMIT_MSG_FNAME = 'message.txt'
DIR_LIST_FNAME = 'directory_listing.txt'


def hash_for(fname):
    with open(fname, 'rb') as fobj:
        contents = fobj.read()
    return sha1(contents).hexdigest()


def parse_message(message):
    msg_info = OrderedDict()
    for line in message.splitlines():
        key, value = line.strip().split(': ', 1)
        key = key.lower()
        if key == 'parents':
            value = value.split()
        msg_info[key] = value
    return msg_info


def info2str(msg_info):
    lines = []
    for key, value in msg_info.items():
        if key in ('old_hash', 'path', 'fixed_parents'):
            continue
        if key == 'parents':
            value = ' '.join(value)
        lines.append('{}: {}\n'.format(key.capitalize(), value))
    return ''.join(lines)


def read_info(message_fname):
    with open(message_fname, 'rt') as fobj:
        message = fobj.read()
    info = parse_message(message)
    info['old_hash'] = sha1(message).hexdigest()
    info['path'] = message_fname
    dir_list_path = pjoin(dirname(message_fname), DIR_LIST_FNAME)
    info['directory hash'] = hash_for(dir_list_path)
    if 'parents' in info:
        info['fixed_parents'] = [False] * len(info['parents'])
    else:
        info['fixed_parents'] = []
    return info


def write_info(msg_info):
    with open(msg_info['path'], 'wt') as fobj:
        fobj.write(info2str(msg_info))


def get_parser():
    parser = ArgumentParser()
    parser.add_argument('root_dir',
                        default=REPO_DIR,
                        nargs='?',
                        help='directory in which to add tree hashes')
    return parser


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


def main():
    """ Process graph in very dumb way """
    args = get_parser().parse_args()
    root_dir = args.root_dir
    # Identify snapshot directories by 'message.txt' files
    globber = pjoin(root_dir, '*', COMMIT_MSG_FNAME)
    infos = []
    for message_fname in glob(globber):
        infos.append(read_info(message_fname))
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
