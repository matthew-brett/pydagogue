# -*- coding: utf-8 -*-
"""
An autorun directive with ``nobel_prize`` as the default directory
"""

from autorun import RunBlock
from writefile import WriteFile

class PrizeRun(RunBlock):
    default_cwd = 'nobel_prize'


class PrizeWrite(WriteFile):
    default_cwd = 'nobel_prize'


def setup(app):
    app.add_directive('prizerun', PrizeRun)
    app.add_directive('prizewrite', PrizeWrite)

# vim: set expandtab shiftwidth=4 softtabstop=4 :
