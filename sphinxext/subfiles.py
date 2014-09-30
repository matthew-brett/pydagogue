# -*- coding: utf-8 -*-
"""
Autorun directives with default directories for:

* myproject
* super
* super/subproject
"""

from autorun import RunBlock, RunCommit

from workrun import OBJECTS_INC


class ProjectRun(RunBlock):
    default_cwd = '/working/myproject'
    default_home = '/working'


class ProjectCommit(RunCommit):
    default_links_file = OBJECTS_INC
    default_cwd = '/working/myproject'
    default_home = '/working'


class SuperRun(RunBlock):
    default_cwd = '/working/super'
    default_home = '/working'


class SuperCommit(RunCommit):
    default_links_file = OBJECTS_INC
    default_cwd = '/working/super'
    default_home = '/working'


class SuperClonedRun(RunBlock):
    default_cwd = '/working/super-cloned'
    default_home = '/working'


class SuperClonedCommit(RunCommit):
    default_links_file = OBJECTS_INC
    default_cwd = '/working/super-cloned'
    default_home = '/working'


class SubProjectRun(RunBlock):
    default_cwd = '/working/super/subproject'
    default_home = '/working'


class SubProjectCommit(RunCommit):
    default_links_file = OBJECTS_INC
    default_cwd = '/working/super/subproject'
    default_home = '/working'


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
