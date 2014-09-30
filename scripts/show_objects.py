#!/usr/bin/env python
from __future__ import print_function

import os
from glob import glob
import zlib

object_glob = os.path.join('.git', 'objects', '??', '*')

for object_fname in glob(object_glob):
    with open(object_fname, 'rb') as fobj:
        contents = zlib.decompress(fobj.read())
    if contents.startswith(b'blob'):
        obj_type = 'blob'
    elif contents.startswith(b'tree'):
        obj_type = 'blob'
    elif contents.startswith(b'commit'):
        obj_type = 'commit'
    elif contents.startswith(b'tag'):
        obj_type = 'tag'
    else:
        raise RuntimeError("I stand corrected")
    print(object_fname, obj_type)
