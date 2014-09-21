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
from subprocess import Popen,PIPE
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
        return self.options.get('env_vars_name', self.default_env_vars_name)

    def _get_env_vars(self):
        env = self.state.document.settings.env
        return getattr(env, self.env_vars_name, {})

    def _set_env_vars(self, env_vars):
        env = self.state.document.settings.env
        return setattr(env, self.env_vars_name, env_vars)

    def add_var(self, name, value):
        vars = self._get_env_vars()
        vars[name] = value
        self._set_env_vars(vars)


class _Params(object):
    pass


class LangMixin(VarsMixin):
    default_cwd = '/'
    default_exe_pre = ''
    default_exe_post = ''

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
        p.prompt_prefix = config.get(language+'_prompt_prefix', '')
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
        exe_pre = self.options.get('exe_pre', self.default_exe_pre)
        exe_post = self.options.get('exe_post', self.default_exe_post)
        exe_code = '\n'.join((exe_pre, p.exe_code, exe_post))
        # Do env substitution
        exe_code = subst_vars(exe_code, self._get_env_vars())
        # Run the code
        stdout, stderr = proc.communicate(exe_code)
        # Process output
        if stdout:
            p.out = ''.join(stdout).decode(p.output_encoding)
        elif stderr:
            p.out = ''.join(stderr).decode(p.output_encoding)
        else:
            p.out = ''
        p.returncode = proc.returncode
        return p


class RunBlock(Directive, LangMixin):
    has_content = True
    required_arguments = 0
    optional_arguments = 1
    final_argument_whitespace = True
    option_spec = {
        'linenos': flag,
        'hide': flag,
        'cwd': unchanged,
        'env_vars_name': unchanged,
        'exe_pre': unchanged,
        'exe_post': unchanged
    }

    def run(self):
        params = self.run_prepare()
        # Get the original code with prefixes
        if params.show_source:
            code = params.prompt_prefix + (
                u'\n' + params.prompt_prefix).join(self.content)
        else:
            code = ''
        code_out = u'\n'.join((code, params.out))
        # Do env substitution
        code_out = subst_vars(code_out, self._get_env_vars())
        # Make nodes
        if 'hide' in self.options:
            return [nodes.comment(code_out, code_out)]
        literal = nodes.literal_block(code_out, code_out)
        literal['language'] = params.language
        literal['linenos'] = 'linenos' in self.options
        return [literal]


SPLITTER_RE = re.compile(r'.. \|(.*)\| replace:: (.*)')


def prefixes_match(prefixes, line):
    match = SPLITTER_RE.match(line)
    if match is None:
        return False
    return match.groups()[0] in prefixes


def add_links(links, link_fname):
    # Write into links file
    link_lines = []
    if os.path.exists(link_fname):
        with open(link_fname, 'rt') as fobj:
            link_lines = fobj.readlines()
    link_lines = [line for line in link_lines
                  if not prefixes_match(links, line)]
    for name, value in links.items():
        link_prefix = '.. |{0}|'.format(name)
        link_line = '{0} replace:: ``{1}``\n'.format(link_prefix, value)
        link_lines.append(link_line)
    with open(link_fname, 'wt') as fobj:
        fobj.write(''.join(link_lines))


class LinksMixin(object):
    default_links_file = '/object_names.inc'

    def add_links(self, links):
        env = self.state.document.settings.env
        links_file = self.options.get('links_file', self.default_links_file)
        _, link_fname = env.relfn2path(links_file)
        # Write links
        add_links(links, link_fname)


class AddVars(Directive, LangMixin, VarsMixin, LinksMixin):
    has_content = True
    required_arguments = 1
    optional_arguments = 1
    final_argument_whitespace = True
    input_encoding = 'ascii'
    option_spec = {
        'runblock_vars': unchanged,
        'links_file': unchanged,
    }

    def run(self):
        name = self.arguments.pop(0)
        params = self.run_prepare()
        value = params.out.strip()
        self.add_var(name, value)
        self.add_links({name: value})
        code = u'\n'.join(self.content)
        return [nodes.comment(code, code)]


def setup(app):
    app.add_directive('runblock', RunBlock)
    app.add_directive('addvars', AddVars)
    app.connect('builder-inited', AutoRun.builder_init)
    app.add_config_value('autorun_languages', AutoRun.config, 'env')

# vim: set expandtab shiftwidth=4 softtabstop=4 :
