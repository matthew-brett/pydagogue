# -*- coding: utf-8 -*-
""" Write a file with given contents using filename on first line
"""

from docutils import nodes
from sphinx.util.compat import Directive
from docutils.parsers.rst.directives import flag, unchanged
from sphinx.errors import SphinxError


class WriteFileError(SphinxError):
    pass


class WriteFile(Directive):
    has_content = True
    required_arguments = 0
    optional_arguments = 1
    default_cwd = '/'
    default_file_prefix = '# file:'
    option_spec = {
        'linenos': flag,
        'hide': flag,
        'cwd': unchanged,
        'file_prefix': unchanged,
    }

    def run(self):
        env = self.state.document.settings.env
        # Build the file text
        cwd = self.options.get('cwd', self.default_cwd)
        # Get the filename
        file_prefix = self.options.get('file_prefix', self.default_file_prefix)
        line0 = self.content[0]
        if not line0.startswith(file_prefix):
            raise WriteFileError('First line should begin with ' + file_prefix)
        fname_sphinx = line0[len(file_prefix):].strip()
        page_content = u'\n'.join(self.content) + '\n'
        file_content = u'\n'.join(self.content[1:]) + '\n'
        # Write the file
        if not fname_sphinx.startswith('/'):
            fname_sphinx = cwd + '/' + fname_sphinx
        _, fname = env.relfn2path(fname_sphinx)
        with open(fname, 'wt') as fobj:
            fobj.write(file_content)
        if 'hide' in self.options:
            return [nodes.comment(page_content, page_content)]
        literal = nodes.literal_block(page_content, page_content)
        literal['linenos'] = 'linenos' in self.options
        return [literal]


def setup(app):
    app.add_directive('writefile', WriteFile)

# vim: set expandtab shiftwidth=4 softtabstop=4 :
