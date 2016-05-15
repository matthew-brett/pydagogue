# -*- coding: utf-8 -*-
"""
Autorun directives with ``working/nobel_prize`` as the default directory
Autorun directives with ``working/repos/nobel_prize`` as the default directory
"""
from os.path import join as pjoin

from autorun import RunBlock, RunCommit
from workrun import WorkVar, OBJECTS_INC
from writefile import WriteFile


class FakeUsbRun(RunBlock):
    default_home = '/working'
    def process_out(self):
        """ Replace the actual remote directory with fake USB directory """
        out = super(FakeUsbRun, self).process_out()
        usb_dir = pjoin(self.state.document.settings.env.srcdir,
                        'working',
                        'repos')
        return out.replace(usb_dir, '/Volumes/my_usb_disk')


class DesktopRun(FakeUsbRun):
    default_cwd = '/working'
    prompt_prefix = '[desktop]$ '


class DesktopOut(DesktopRun):
    """ For displaying output only, with no highlighting
    """
    opt_defaults = {'highlighter': 'none', 'hide-code': True}


class PrizeRun(DesktopRun):
    default_cwd = '/working/nobel_prize'


class PrizeWrite(WriteFile):
    default_cwd = '/working/nobel_prize'


class PrizeCommit(RunCommit):
    default_links_file = OBJECTS_INC
    prompt_prefix = '[desktop]$ '
    default_home = '/working'
    default_cwd = '/working/nobel_prize'


class PrizeVar(WorkVar):
    default_cwd = '/working/nobel_prize'


class PrizeOut(PrizeRun):
    """ For displaying output only, with no highlighting
    """
    opt_defaults = {'highlighter': 'none', 'hide-code': True}


class LaptopRun(FakeUsbRun):
    prompt_prefix = '[laptop]$ '
    default_cwd = '/working/repos'


class PrizeLapRun(LaptopRun):
    default_cwd = '/working/repos/nobel_prize'


class PrizeLapCommit(RunCommit):
    default_links_file = OBJECTS_INC
    prompt_prefix = '[laptop]$ '
    default_home = '/working'
    default_cwd = '/working/repos/nobel_prize'


def setup(app):
    app.add_directive('desktoprun', DesktopRun)
    app.add_directive('desktopout', DesktopOut)
    app.add_directive('prizerun', PrizeRun)
    app.add_directive('prizecommit', PrizeCommit)
    app.add_directive('prizevar', PrizeVar)
    app.add_directive('prizeout', PrizeOut)
    app.add_directive('prizewrite', PrizeWrite)
    app.add_directive('laptoprun', LaptopRun)
    app.add_directive('prizelaprun', PrizeLapRun)
    app.add_directive('prizelapcommit', PrizeLapCommit)

# vim: set expandtab shiftwidth=4 softtabstop=4 :
