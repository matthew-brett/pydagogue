""" Testing prizefiles module
"""

from os.path import join as pjoin, split as psplit, abspath, dirname
import sys
from tempfile import mkdtemp
import shutil

sys.path.insert(0, abspath(pjoin(dirname(__file__), '..')))

from autorun import add_links, prefixes_match

from nose.tools import (assert_true, assert_false, assert_raises,
                        assert_equal, assert_not_equal)


def assert_file_equal_string(fname, text):
    with open(fname, 'rt') as fobj:
        contents = fobj.read()
    assert_equal(contents, text)


def test_prefixes_match():
    links = {'name': 'commit'}
    assert_true(prefixes_match(links, '.. |name| replace:: something'))
    assert_true(prefixes_match(links, '.. |name| replace:: something\n'))
    assert_false(prefixes_match(links, '.. |aname| replace:: something'))
    links['aname'] = 'content'
    assert_true(prefixes_match(links, '.. |name| replace:: something'))
    assert_true(prefixes_match(links, '.. |aname| replace:: something'))


def test_add_links():
    tmpdir = mkdtemp()
    links_fname = pjoin(tmpdir, 'links.inc')
    try:
        add_links({'name': 'commit'}, links_fname)
        assert_file_equal_string(links_fname,
                                 ".. |name| replace:: ``commit``\n")
        add_links({'name': 'commit'}, links_fname)
        assert_file_equal_string(links_fname,
                                 ".. |name| replace:: ``commit``\n")
        add_links({'name2': 'commit2'}, links_fname)
        assert_file_equal_string(links_fname,
""".. |name| replace:: ``commit``
.. |name2| replace:: ``commit2``
""")
    finally:
        shutil.rmtree(tmpdir)
