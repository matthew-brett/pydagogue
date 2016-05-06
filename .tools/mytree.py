""" A little utility to display the structure of directory trees

Don't worry about the detail here, you'll see below what it does.
The code is not complicated, but it's not relevant to the main points on git.

Inspired by:

http://lorenzod8n.wordpress.com/2007/12/13/creating-a-tree-utility-in-python-part-2/

with thanks.

This version is my own copyright (Matthew Brett) released under 2-clause BSD
"""
from __future__ import print_function, division

from os import getcwd, listdir, stat
from os.path import isdir, basename
import re

try:
    string_type = basestring
except NameError:
    string_type = str

# Unicode constants for constructing the tree trunk and branches
ALONG = u'\u2500'
DOWN = u'\u2502'
DOWN_RIGHT = u'\u251c'
ELBOW_RIGHT = u'\u2514'
BLUE = u'\033[94m'
ENDC = u'\033[0m'
DOWN_RIGHT_ALONG = DOWN_RIGHT + ALONG * 2 + u" "
ELBOW_RIGHT_ALONG = ELBOW_RIGHT + ALONG * 2 + u" "
CONTINUE_INDENT = DOWN + u' ' * 3
FINISH_INDENT = u' ' * 4

# File sizes
KB = 1024
MB = KB * KB
GB = MB * KB


def show_tree(root_path=None,
              indent_str=u'',
              show_size=False,
              dir_sort_func=None,
              elide_dirs=None):
    """ Return string with tree structure starting from `root_path`

    Parameters
    ----------
    root_path : None or str, optional
        path from which to print directory tree structure.  If None, use
        current directory.
    indent_str : str, optional
        prefix to print for every entry in the tree.  Usually '', and then set
        by recursion into the function when printing subdirectories.
    show_size : {False, True}, optional
        If True, show size next to file name in human readable format.
    dir_sort_func : None or callable, optional
        If None, sort directory entries by name.  If callable, call with single
        argument ``path`` to return directory entries in desired order.  Paths
        returned are full paths.
    elide_dirs : None or str or regexp or callable.
        str containing regexp or regexp or callable identifying directories for
        which to elide contents.  Elide if regexp matches or callable returns
        True.  Callable accepts single argument ``path``.

    Returns
    -------
    tree_str : str
        String representing tree
    """
    if root_path is None:
        root_path = getcwd()
    if dir_sort_func is None:
        dir_sort_func = lambda path: sorted(listdir(path))
    if elide_dirs is None:
        elider = lambda path : False
    elif isinstance(elide_dirs, string_type):
        elide_re = re.compile(elide_dirs)
        elider = lambda path: elide_re.search(path) != None
    elif hasattr(elide_dirs, 'search'):
        elider = lambda path: elide_re.search(path) != None
    else:
        elider = elide_dirs
    # ensure return of unicode paths from listdir
    root_path = unicode(root_path)
    # Full paths returned
    paths = dir_sort_func(root_path)
    if len(paths) == 0:
        return
    lines = []
    for path in paths:
        lines.append(path_lines(path,
                                indent_str,
                                show_size,
                                dir_sort_func,
                                elider,
                                path == paths[-1]))
    return '\n'.join(lines)


def human_size(size):
    for divisor, suffix in ((GB, 'G'),
                            (MB, 'M'),
                            (KB, 'K')):
        divided = size / divisor
        if divided < 1:
            continue
        if round(divided) < 10:
            return '{:.1f}{}'.format(divided, suffix)
        return '{:.0f}{}'.format(round(divided), suffix)
    return '{:d}B'.format(size)


def color_path(path):
    return BLUE + path + ENDC


def path_lines(path, indent_str, show_size=False, dir_sort_func=None,
               elider=lambda p: False, last_entry=False):
    """ Return str for single `path`

    Parameters
    ----------
    path : str
        file name or directory name
    indent_str : str
        string to prefix to entry for this `path`
    show_size : {False, True}, optional
        If True, show size next to file name in human readable format.
    dir_sort_func : None or callable, optional
        If None, sort directory entries by name.  If callable, call with single
        argument ``path`` to return directory entries in desired order.  Paths
        returned are full paths.
    elider : callable, optional
        Callable accepting single argument ``path``, returning True if we
        should elide the contents of directory ``path``.
    last_entry : bool, optional
        Whether this is the last entry in a list of paths.

    Returns
    -------
    path_lines : str
        String representing this path.  If `path` is a directory will have one
        line per entry in the directory.
    """
    have_dir = isdir(path)
    sub_path = basename(path)
    leader = ELBOW_RIGHT_ALONG if last_entry else DOWN_RIGHT_ALONG
    path_colored = color_path(sub_path) if have_dir else sub_path
    path_str = indent_str + leader + path_colored
    if show_size and not have_dir:
        size = stat(path).st_size
        path_str += u' [{}]'.format(human_size(size))
    if not have_dir:
        return path_str
    extra_indent = FINISH_INDENT if last_entry else CONTINUE_INDENT
    indent_str += extra_indent
    if elider(path):
        return u'{}\n{}...'.format(path_str, indent_str)
    subdir_lines = show_tree(path,
                             indent_str,
                             show_size,
                             dir_sort_func)
    if subdir_lines:
        path_str = path_str + '\n' + subdir_lines
    return path_str
