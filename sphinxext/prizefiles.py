# -*- coding: utf-8 -*-
"""
Autorun directives with ``nobel_prize`` as the default directory
"""
from os.path import join as pjoin

from autorun import RunBlock, CmdAddVar, RunCommit
from writefile import WriteFile


class FakeUsbRun(RunBlock):
    def process_out(self):
        """ Replace the actual remote directory with fake USB directory """
        out = super(FakeUsbRun, self).process_out()
        usb_dir = pjoin(self.state.document.settings.env.srcdir, 'my_repos')
        return out.replace(usb_dir, '/Volumes/my_usb_disk')


class DesktopRun(FakeUsbRun):
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


class PrizeVar(CmdAddVar):
    default_cwd = 'nobel_prize'


class LaptopRun(FakeUsbRun):
    prompt_prefix = '[laptop]$ '
    default_cwd = 'my_repos'
    default_home = '/fake_home'


class PrizeLapRun(LaptopRun):
    default_cwd = 'my_repos/nobel_prize'


class PrizeLapCommit(RunCommit):
    prompt_prefix = '[laptop]$ '
    default_home = '/fake_home'
    default_cwd = 'my_repos/nobel_prize'


def setup(app):
    app.add_directive('desktoprun', DesktopRun)
    app.add_directive('prizerun', PrizeRun)
    app.add_directive('prizecommit', PrizeCommit)
    app.add_directive('prizevar', PrizeVar)
    app.add_directive('prizewrite', PrizeWrite)
    app.add_directive('laptoprun', LaptopRun)
    app.add_directive('prizelaprun', PrizeLapRun)
    app.add_directive('prizelapcommit', PrizeLapCommit)

# vim: set expandtab shiftwidth=4 softtabstop=4 :
