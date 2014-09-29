# -*- coding: utf-8 -*-
"""
Autorun directives with ``working`` as the default directory
"""

from autorun import RunBlock, CmdAddVar


class WorkRun(RunBlock):
    default_cwd = '/working'


class WorkVar(CmdAddVar):
    default_links_file = '/object_names.inc'
    default_cwd = '/working'


def setup(app):
    app.add_directive('workrun', WorkRun)
    app.add_directive('workvar', WorkVar)

# vim: set expandtab shiftwidth=4 softtabstop=4 :
