# -*- coding: utf-8 -*-
"""
An autorun directive with ``nobel_prize`` as the default directory
"""

import os
from subprocess import check_output

from docutils.parsers.rst.directives import flag, unchanged

from autorun import RunBlock
from writefile import WriteFile

class PrizeRun(RunBlock):
    default_cwd = 'nobel_prize'


class PrizeWrite(WriteFile):
    default_cwd = 'nobel_prize'


def backtick(*args, **kwargs):
    """ Get command output as stripped string """
    output = check_output(*args, **kwargs)
    return output.decode('latin1').strip()


class PrizeCommit(RunBlock):
    """ Do a runblock with a commit in it somewhere """
    required_arguments = 3
    default_cwd = 'nobel_prize'
    default_links_file = '/commit_names.inc'
    option_spec = {
        'linenos': flag,
        'hide': flag,
        'cwd': unchanged,
        'links_file': unchanged,
    }

    def run(self):
        name, date, time = self.arguments[0:3]
        assert len(self.arguments) == 3 or self.arguments[3] == 'bash'
        self.arguments[:] = []
        env = self.state.document.settings.env
        links_file = self.options.get('links_file', self.default_links_file)
        _, link_fname = env.relfn2path(links_file)
        # Add lines setting git dates
        self.exe_pre = \
"""export GIT_AUTHOR_DATE="{date}T{time}"
export GIT_COMMITTER_DATE="{date}T{time}"
""".format(date=date, time=time)
        # Execute code, return nodes to insert
        nodes = RunBlock.run(self)
        # Get git commit hash
        _, cwd = env.relfn2path(self.options.get('cwd', self.default_cwd))
        commit = backtick(['git', 'rev-parse', 'HEAD'], cwd=cwd)
        # Insert into names dict
        vars = self._get_env_vars()
        vars[name] = commit
        self._set_env_vars(vars)
        # Write into links file
        link_prefix = '.. |{0}|'.format(name)
        link_line = '{0} replace:: {1}\n'.format(link_prefix, commit)
        link_lines = []
        if os.path.exists(link_fname):
            with open(link_fname, 'rt') as fobj:
                link_lines = fobj.readlines()
        link_lines = [line for line in link_lines
                      if not line.startswith(link_prefix)]
        with open(link_fname, 'wt') as fobj:
            fobj.write(''.join(link_lines + [link_line]))
        return nodes


def setup(app):
    app.add_directive('prizerun', PrizeRun)
    app.add_directive('prizecommit', PrizeCommit)
    app.add_directive('prizewrite', PrizeWrite)

# vim: set expandtab shiftwidth=4 softtabstop=4 :
