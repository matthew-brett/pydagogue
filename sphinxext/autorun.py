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


class RunBlock(Directive):
    has_content = True
    required_arguments = 0
    optional_arguments = 1
    final_argument_whitespace = True
    option_spec = {
        'linenos': flag,
        'hide': flag,
        'cwd': unchanged,
    }

    def run(self):
        env = self.state.document.settings.env
        config = AutoRun.config
        try:
            language = self.arguments[0]
        except IndexError:
            language = 'bash'
        print 'opts', self.options

        if language not in config:
            raise RunBlockError('Unknown language %s' % language)

        # Get configuration values for the language
        args = config[language].split()
        input_encoding = config.get(language+'_input_encoding','ascii')
        output_encoding = config.get(language+'_output_encoding','ascii')
        prefix_chars = config.get(language+'_prefix_chars', 0)
        show_source = config.get(language+'_show_source', True)
        prompt_prefix = config.get(language+'_prompt_prefix', '')

        # Build the code text
        _, cwd = env.relfn2path(self.options.get('cwd', '/'))
        proc = Popen(args,bufsize=1,stdin=PIPE,stdout=PIPE,stderr=PIPE,
                     cwd=cwd)
        codelines = (line[prefix_chars:] for line in self.content)
        code = u'\n'.join(codelines).encode(input_encoding)

        # Run the code
        stdout, stderr = proc.communicate(code)

        # Process output
        if stdout:
            out = ''.join(stdout).decode(output_encoding)
        elif stderr:
            out = ''.join(stderr).decode(output_encoding)
        else:
            out = ''

        # Get the original code with prefixes
        if show_source:
            code = prompt_prefix + (u'\n' + prompt_prefix).join(self.content)
        else:
            code = ''
        code_out = u'\n'.join((code,out))

        if 'hide' in self.options:
            return [nodes.comment(code_out, code_out)]

        literal = nodes.literal_block(code_out, code_out)
        literal['language'] = language
        literal['linenos'] = 'linenos' in self.options
        return [literal]


def setup(app):
    app.add_directive('runblock', RunBlock)
    app.connect('builder-inited', AutoRun.builder_init)
    app.add_config_value('autorun_languages', AutoRun.config, 'env')

# vim: set expandtab shiftwidth=4 softtabstop=4 :
