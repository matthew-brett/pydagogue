# -*- coding: utf-8 -*-
"""
Autorun directives with ``subfiles`` as the default directory
"""

from autorun import RunBlock, RunCommit

class ProjectRun(RunBlock):
    default_cwd = 'myproject'
    default_home = '/fake_home'


class ProjectCommit(RunCommit):
    default_cwd = 'myproject'
    default_home = '/fake_home'


class SuperRun(RunBlock):
    default_cwd = 'super'
    default_home = '/fake_home'


class SuperCommit(RunCommit):
    default_cwd = 'super'
    default_home = '/fake_home'


class SuperClonedRun(RunBlock):
    default_cwd = 'super-cloned'
    default_home = '/fake_home'


class SuperClonedCommit(RunCommit):
    default_cwd = 'super-cloned'
    default_home = '/fake_home'


class SubProjectRun(RunBlock):
    default_cwd = 'super/subproject'
    default_home = '/fake_home'


class SubProjectCommit(RunCommit):
    default_cwd = 'super/subproject'
    default_home = '/fake_home'


def setup(app):
    app.add_directive('projectrun', ProjectRun)
    app.add_directive('superrun', SuperRun)
    app.add_directive('superclonedrun', SuperClonedRun)
    app.add_directive('subprojectrun', SubProjectRun)
    app.add_directive('projectcommit', ProjectCommit)
    app.add_directive('supercommit', SuperCommit)
    app.add_directive('superclonedcommit', SuperClonedCommit)
    app.add_directive('subprojectcommit', SubProjectCommit)

# vim: set expandtab shiftwidth=4 softtabstop=4 :
