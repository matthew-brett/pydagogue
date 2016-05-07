""" Apply ordering to directories in base repo

Print out directory using some custom ordering
"""
from __future__ import print_function

import sys
from os import listdir
from os.path import (dirname, join as pjoin, abspath, isdir, isfile, basename,
                     sep as dir_sep)
from time import strptime, mktime, localtime
import re

MY_PATH = abspath(dirname(__file__))
DIR_PATH = abspath(pjoin(MY_PATH, '..'))

COMMIT_MSG_FNAME = 'message.txt'

DATE_FMT = 'Date: %B %d %Y, %H.%M'

NOW = mktime(localtime())
KNOWNS = {'staging': NOW,
          'working': NOW + 1}

SNAPSHOT_RE = re.compile(r'snapshot_(\d+)')

sys.path.append(MY_PATH)
from mytree import show_tree, color_path


def msg_to_secs(msg_file):
    with open(msg_file, 'rt') as fobj:
        for line in fobj:
            if line.startswith('Date'):
                break
        else:
            return
    return mktime(strptime(line.strip(), DATE_FMT))


def sortkey_from_dir(path):
    base = basename(path)
    if base in KNOWNS:
        return KNOWNS[base]
    snap_match = SNAPSHOT_RE.match(base)
    if snap_match:
        return int(snap_match.groups()[0])
    msg_path = pjoin(path, COMMIT_MSG_FNAME)
    if isfile(msg_path):
        return msg_to_secs(msg_path)
    return base


def sortkey_from_file(path):
    base = basename(path)
    if base == COMMIT_MSG_FNAME:
        return 'zzz' + base
    return base


def dir_sort_func(path):
    files = []
    dirs = []
    for p in listdir(path):
        if p.startswith('.'):
            continue
        full_p = pjoin(path, p)
        if isdir(full_p):
            dirs.append(full_p)
        elif isfile(full_p):
            files.append(full_p)
    dirs = sorted(dirs, key=sortkey_from_dir)[::-1]
    files = sorted(files, key=sortkey_from_file)
    return dirs + files


def main():
    root_dir = DIR_PATH if len(sys.argv) <= 1 else sys.argv[1].decode('latin1')
    hasta = None if len(sys.argv) <= 2 else sys.argv[2].decode('latin1')
    # Basename needs slash removed
    if root_dir.endswith(dir_sep):
        root_dir = root_dir[:-1]
    print(color_path(basename(root_dir)))
    res = show_tree(root_dir, show_size=True, dir_sort_func=dir_sort_func)
    if res is None:
        return
    for line in res.splitlines():
        if hasta and hasta in line:
            print('...')
            break
        print(line)


if __name__ == '__main__':
    main()
