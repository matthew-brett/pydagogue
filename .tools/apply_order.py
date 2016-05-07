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
from locale import getpreferredencoding
from argparse import ArgumentParser

MY_PATH = abspath(dirname(__file__))
ENCODING = getpreferredencoding()

# Name of the commit message file, used for retrieving commit date
COMMIT_MSG_FNAME = 'message.txt'

# Format of date recorded in commit message file
DATE_FMT = 'Date: %B %d %Y, %H.%M'

# Directories will later be sorted by time, with latest first.  Set known
# directories to be at the top by giving them now + something times.
_now = mktime(localtime())
_known_dirs = ('repo', 'staging', 'working')
KNOWNS = dict(zip(_known_dirs, [_now + i for i in range(len(_known_dirs))]))

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


def get_parser():
    default_path = abspath(pjoin(MY_PATH, '..'))
    parser = ArgumentParser()
    parser.add_argument('root_dir',
                        default=default_path,
                        nargs='?',
                        help='directory for which to show tree repr')
    parser.add_argument('--hasta', type=str,
                        help='regex matching line before which to '
                        'truncate output')
    parser.add_argument('--elide-dir', action='append',
                       help='regex(es) for directories to elide')
    return parser


def make_elider(elide_strs):
    if not elide_strs:  # Empty or None
        return lambda p : False
    elide_res = [re.compile(elide_re) for elide_re in elide_strs]

    def elider(path):
        for elide_re in elide_res:
            if elide_re.search(path):
                return True
        return False

    return elider


def printout(s):
    sys.stdout.write((s + '\n').encode(ENCODING))


def main():
    args = get_parser().parse_args()
    # Basename needs slash removed
    root_dir = args.root_dir
    if root_dir.endswith(dir_sep):
        root_dir = root_dir[:-1]
    elider = make_elider(args.elide_dir)
    hasta = re.compile(args.hasta) if args.hasta else None
    printout(color_path(basename(root_dir)))
    res = show_tree(root_dir, show_size=True, dir_sort_func=dir_sort_func,
                    elide_dirs=elider)
    if res is None:
        return
    for line in res.splitlines():
        if hasta and hasta.search(line):
            printout('...')
            break
        printout(line)


if __name__ == '__main__':
    main()
