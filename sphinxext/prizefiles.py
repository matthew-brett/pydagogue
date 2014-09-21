# -*- coding: utf-8 -*-
"""
An autorun directive with ``nobel_prize`` as the default directory
"""

from subprocess import check_output

from docutils.parsers.rst.directives import flag, unchanged

from autorun import RunBlock, LinksMixin, AddVars
from writefile import WriteFile

class PrizeRun(RunBlock):
    default_cwd = 'nobel_prize'


class PrizeWrite(WriteFile):
    default_cwd = 'nobel_prize'


def backtick(*args, **kwargs):
    """ Get command output as stripped string """
    output = check_output(*args, **kwargs)
    return output.decode('latin1').strip()


class PrizeCommit(RunBlock, LinksMixin):
    """ Do a runblock with a commit in it somewhere """
    required_arguments = 3
    default_cwd = 'nobel_prize'
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
        # Add lines setting git dates
        self.default_exe_pre = \
"""export GIT_AUTHOR_DATE="{date}T{time}"
export GIT_COMMITTER_DATE="{date}T{time}"
""".format(date=date, time=time)
        # Execute code, return nodes to insert
        nodes = RunBlock.run(self)
        # Get git commit hash
        _, cwd = env.relfn2path(self.options.get('cwd', self.default_cwd))
        commit = backtick(['git', 'rev-parse', 'HEAD'], cwd=cwd)
        # Insert into names dict
        self.add_var(name, commit)
        # Write links
        self.add_links({name: commit, name + '-7': commit[:7]})
        return nodes


class PrizeVars(AddVars):
    default_cwd = 'nobel_prize'


def setup(app):
    app.add_directive('prizerun', PrizeRun)
    app.add_directive('prizecommit', PrizeCommit)
    app.add_directive('prizevars', PrizeVars)
    app.add_directive('prizewrite', PrizeWrite)

# vim: set expandtab shiftwidth=4 softtabstop=4 :
