# -*- coding: utf-8 -*-
"""
Autorun directives with ``nobel_prize`` as the default directory
"""

from autorun import RunBlock, AddVars, RunCommit
from writefile import WriteFile

class DesktopRun(RunBlock):
    prompt_prefix = '[desktop]$ '


class PrizeRun(DesktopRun):
    default_cwd = 'nobel_prize'
    default_home = '/fake_home'


class PrizeWrite(WriteFile):
    default_cwd = 'nobel_prize'


class PrizeCommit(RunCommit):
    prompt_prefix = '[desktop]$ '
    default_home = '/fake_home'
    default_cwd = 'nobel_prize'


class PrizeVars(AddVars):
    default_cwd = 'nobel_prize'


def setup(app):
    app.add_directive('desktoprun', DesktopRun)
    app.add_directive('prizerun', PrizeRun)
    app.add_directive('prizecommit', PrizeCommit)
    app.add_directive('prizevars', PrizeVars)
    app.add_directive('prizewrite', PrizeWrite)

# vim: set expandtab shiftwidth=4 softtabstop=4 :
