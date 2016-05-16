# -*- coding: utf-8 -*-
"""
Based on:

sphinxcontrib.autorun
~~~~~~~~~~~~~~~~~~~~~~

Run the code and insert stdout after the code block.

    :copyright: Copyright 2007-2009 by the Sphinx team, see AUTHORS.
    :license: BSD, see LICENSE for details.

Here's the LICENSE referred to:

If not otherwise noted, the extensions in this package are licensed
under the following license.

Copyright (c) 2009 by the contributors (see AUTHORS file).
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are
met:

* Redistributions of source code must retain the above copyright
  notice, this list of conditions and the following disclaimer.

* Redistributions in binary form must reproduce the above copyright
  notice, this list of conditions and the following disclaimer in the
  documentation and/or other materials provided with the distribution.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
"AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""
import os
from subprocess import Popen, PIPE
import re

from docutils import nodes
from sphinx.util.compat import Directive
from docutils.parsers.rst.directives import flag, unchanged
from sphinx.errors import SphinxError


class RunBlockError(SphinxError):
    pass
    # category = 'runblock error'


class AutoRun(object):
    here = os.path.abspath(__file__)
    pycon = os.path.join(os.path.dirname(here), 'pycon.py')
    config = dict(
        pycon = 'python ' + pycon,
        pycon_prefix_chars = 4,
        pycon_show_source = False,
        console = 'bash',
        console_prefix_chars = 1,
        bash = 'bash',
        bash_prefix_chars = 0,
        bash_prompt_prefix = '$ ',
        bash_output_encoding = 'utf8',
    )

    @classmethod
    def builder_init(cls,app):
        cls.config.update(app.builder.config.autorun_languages)


def subst_vars(in_str, vars):
    """ Do jinja-like variable substitution """
    out_str = in_str
    for key, value in vars.items():
        out_str = re.sub('{{ ' + key + ' }}', value, out_str)
    return out_str


class VarsMixin(object):
    default_env_vars_name = 'runblock_vars'

    @property
    def env_vars_name(self):
        return self.options.get('env-vars-name', self.default_env_vars_name)

    @property
    def env_vars(self):
        env = self.state.document.settings.env
        if not hasattr(env, self.env_vars_name):
            setattr(env,
                    self.env_vars_name,
                    dict(common = {},
                         run = {},
                         render = {}))
        return getattr(env, self.env_vars_name)

    def add_typed_var(self, name, value, var_type):
        self.env_vars[var_type][name] = value

    def get_typed_vars(self, var_type):
        out = self.env_vars['common'].copy()
        if var_type in ('run', 'render'):
            out.update(self.env_vars[var_type])
        elif not var_type == 'common':
            raise ValueError('var_type should be in {common, run, render}')
        return out


class _Params(object):
    pass


class LangMixin(VarsMixin):
    default_cwd = '/'
    default_exe_pre = ''
    default_exe_post = ''
    default_home = None
    prompt_prefix = None

    def run_prepare(self):
        p = _Params()
        env = self.state.document.settings.env
        config = AutoRun.config
        try:
            language = self.arguments[0]
        except IndexError:
            language = 'bash'

        if language not in config:
            raise RunBlockError('Unknown language %s' % language)

        # Get configuration values for the language
        args = config[language].split()
        p.language = language
        p.input_encoding = config.get(language+'_input_encoding','ascii')
        p.output_encoding = config.get(language+'_output_encoding','ascii')
        p.prefix_chars = config.get(language+'_prefix_chars', 0)
        p.show_source = config.get(language+'_show_source', True)
        lang_prefix = config.get(language + '_prompt_prefix', '')
        p.prompt_prefix = (lang_prefix if self.prompt_prefix is None
                           else self.prompt_prefix)
        # Build the code text
        _, p.cwd = env.relfn2path(self.options.get('cwd', self.default_cwd))
        proc = Popen(args,
                     bufsize=1,
                     stdin=PIPE,
                     stdout=PIPE,
                     stderr=PIPE,
                     cwd=p.cwd)
        # Remove prefix
        p.codelines = (line[p.prefix_chars:] for line in self.content)
        # Make executable code
        p.exe_code = u'\n'.join(p.codelines).encode(p.input_encoding)
        # Prepost, postpend extra code lines
        exe_pre = self.options.get('exe-pre', self.default_exe_pre)
        exe_post = self.options.get('exe-post', self.default_exe_post)
        home = self.options.get('home', self.default_home)
        # Get home directory
        if  home not in (None, '~'):
            _, home_dir = env.relfn2path(home)
            exe_pre = '\n'.join(('export HOME=' + home_dir, exe_pre))
        if exe_pre:
            p.exe_code = '{0}\n{1}'.format(exe_pre, p.exe_code)
        if exe_post:
            p.exe_code = '{0}\n{1}'.format(p.exe_code, exe_post)
        # Do env substitution
        exe_code = subst_vars(p.exe_code, self.get_typed_vars('run'))
        # Run the code
        stdout, stderr = proc.communicate(exe_code)
        # Process output
        p.out = u''
        if stdout:
            p.out += stdout.decode(p.output_encoding)
        if stderr:
            p.out += stderr.decode(p.output_encoding)
        p.returncode = proc.returncode
        self.params = p


class RunBlock(Directive, LangMixin):
    has_content = True
    required_arguments = 0
    optional_arguments = 1
    final_argument_whitespace = True
    option_spec = {
        'linenos': flag,
        'hide': flag,
        'hide-code': flag,
        'hide-out': flag,
        'highlighter': unchanged,
        'cwd': unchanged,
        'env-vars-name': unchanged,
        'exe-pre': unchanged,
        'exe-post': unchanged,
        'home': unchanged,
        'allow-fail': flag,
    }
    opt_defaults = {}

    def run(self):
        # Set default options
        self.set_opt_defaults()
        # Run code, collect output
        self.run_prepare()
        if not 'allow-fail' in self.options and self.params.returncode != 0:
            raise RuntimeError('Command {} failed with {} in doc {}'.format(
                self.params.exe_code,
                self.params.out,
                self.state.document['source']))
        params = self.params
        # Get the original code with prefixes
        if params.show_source:
            code = params.prompt_prefix + (
                u'\n' + params.prompt_prefix).join(self.content)
        else:
            code = ''
        # Do post-run env substitution on code
        code = subst_vars(code, self.get_typed_vars('render'))
        # Do output post-processing
        out = self.process_out()
        # String for rendering
        code_out = u'\n'.join((code, out))
        if 'hide-code' in self.options:
            contents = out
        elif 'hide-out' in self.options:
            contents = code
        else:
            contents = code_out
        # Make nodes
        if 'hide' in self.options:
            return [nodes.comment(code_out, code_out)]
        literal = nodes.literal_block(contents, contents)
        literal['language'] = (self.options['highlighter']
                               if 'highlighter' in self.options
                               else params.language)
        literal['linenos'] = 'linenos' in self.options
        return [literal]

    def process_out(self):
        """ A hook to add extra processing for out
        """
        return self.params.out

    def set_opt_defaults(self):
        """ Set default options """
        for key, value in self.opt_defaults.items():
            if key not in self.options:
                self.options[key] = value


SPLITTER_RE = re.compile(r'.. \|(.*)\| replace:: (.*)')


def prefixes_match(prefixes, line):
    match = SPLITTER_RE.match(line)
    if match is None:
        return False
    return match.groups()[0] in prefixes


def add_links(links, link_fname, literal=True):
    # Write into links file
    link_lines = []
    if os.path.exists(link_fname):
        with open(link_fname, 'rt') as fobj:
            link_lines = fobj.readlines()
    link_lines = [line for line in link_lines
                  if not prefixes_match(links, line)]
    literal_markup = '``' if literal else ''
    for name, value in links.items():
        link_prefix = '.. |{name}|'.format(name=name)
        link_line = '{prefix} replace:: {markup}{value}{markup}\n'.format(
            prefix=link_prefix, value=value, markup=literal_markup)
        link_lines.append(link_line)
    with open(link_fname, 'wt') as fobj:
        fobj.write(''.join(link_lines))


class LinksMixin(object):
    default_links_file = '/dynamic_names.inc'

    def add_links(self, links, literal=True):
        env = self.state.document.settings.env
        links_file = self.options.get('links_file', self.default_links_file)
        _, link_fname = env.relfn2path(links_file)
        # Write links
        add_links(links, link_fname, literal)


class CmdAddVar(Directive, LangMixin, VarsMixin, LinksMixin):
    """ Define variables to use during run / render of code blocks

    Variables can be of three types:

    * 'run' : variables available for use in code, substituted before code is
      run;
    * 'render' : variables substituted after code has run;
    * 'common' : variables defined for both 'run' and 'render'.

    Variable substitution if of jinja type with "Some {{ var }} here" becoming
    "some var_value here" where ``var = 'var_value'``.

    Of course, you'll nearly always have to define both a 'run' and a 'render'
    version of the same-named variable, otherwise the "{{ var }}" part of the
    expression will either break your code ('run' not defined) or look bad
    ('render' not defined).
    """
    has_content = True
    required_arguments = 1
    optional_arguments = 1
    final_argument_whitespace = True
    input_encoding = 'ascii'
    option_spec = {
        'runblock_vars': unchanged,
        'links_file': unchanged,
        'omit_link': flag,
        'var_type': unchanged,
        'not-literal': flag,
    }

    def run(self):
        name = self.arguments.pop(0)
        self.run_prepare()
        value = self.params.out.strip()
        var_type = self.options.get('var_type', 'common')
        self.add_typed_var(name, value, var_type)
        literal = not 'not-literal' in self.options
        if 'omit_link' not in self.options:
            self.add_links({name: value}, literal=literal)
        code = u'\n'.join(self.content)
        return [nodes.comment(code, code)]


class RunCommit(RunBlock, LinksMixin):
    """ Do a runblock with a commit in it somewhere """
    required_arguments = 3 # name, date, time
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
        proc = Popen(['git', 'rev-parse', 'HEAD'], stdout=PIPE, cwd=cwd)
        stdout, stderr = proc.communicate()
        commit = stdout.decode(self.params.output_encoding).strip()
        # Insert into names dict
        self.add_typed_var(name, commit, 'common')
        self.add_typed_var(name + '_7', commit[:7], 'common')
        # Write links
        self.add_links({name: commit, name + '_7': commit[:7]})
        return nodes


def setup(app):
    app.add_directive('runblock', RunBlock)
    app.add_directive('runcommit', RunCommit)
    app.add_directive('cmdaddvar', CmdAddVar)
    app.connect('builder-inited', AutoRun.builder_init)
    app.add_config_value('autorun_languages', AutoRun.config, 'env')

# vim: set expandtab shiftwidth=4 softtabstop=4 :
