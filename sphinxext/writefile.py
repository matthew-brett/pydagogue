# -*- coding: utf-8 -*-
""" Write a file with given contents using filename on first line
"""

from docutils import nodes
from sphinx.util.compat import Directive
from docutils.parsers.rst.directives import flag, unchanged
from sphinx.errors import SphinxError

class FileContents(nodes.Admonition, nodes.Element):
    pass


def visit_todo_node(self, node):
    self.visit_admonition(node)


def depart_todo_node(self, node):
    self.depart_admonition(node)


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
        'language': unchanged,
    }

    def run(self):
        env = self.state.document.settings.env
        # Default language
        language = self.options.get('language')
        # Build the file text
        cwd = self.options.get('cwd', self.default_cwd)
        # Get the filename
        file_prefix = self.options.get('file_prefix', self.default_file_prefix)
        line0 = self.content[0]
        if not line0.startswith(file_prefix):
            raise WriteFileError('First line should begin with ' + file_prefix)
        fname_raw = line0[len(file_prefix):].strip()
        file_content = u'\n'.join(self.content[1:]) + '\n'
        # Write the file
        if not fname_raw.startswith('/'):
            if cwd == '/':
                fname_sphinx = cwd + fname_raw
            else:
                fname_sphinx = cwd + '/' + fname_raw
        else:
            fname_sphinx = fname_raw
        _, fname = env.relfn2path(fname_sphinx)
        with open(fname, 'wt') as fobj:
            fobj.write(file_content)
        if 'hide' in self.options:
            return [nodes.comment(file_content, file_content)]
        literal = nodes.literal_block(file_content, file_content)
        if not language is None:
            literal['language'] = language
        literal['linenos'] = 'linenos' in self.options
        para = FileContents()
        para += nodes.emphasis(text='Contents of ')
        para += nodes.literal(text=fname_raw)
        para += literal
        return [para]


def setup(app):
    app.add_node(FileContents,
                 html=(visit_todo_node, depart_todo_node),
                 latex=(visit_todo_node, depart_todo_node),
                 text=(visit_todo_node, depart_todo_node))
    app.add_directive('writefile', WriteFile)

# vim: set expandtab shiftwidth=4 softtabstop=4 :
