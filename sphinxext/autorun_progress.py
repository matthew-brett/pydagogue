# -*- coding: utf-8 -*-
"""Drop partial percent-progress updates from ``runblock`` output.

Subclass of :class:`sphinx_autorun.RunBlock`.  A progress run is a series of
percent updates (git's ``label: N% (n/n)`` lines, or a meter such as
``1%  31 KiB  13 MiB/s 0s`` redrawn with carriage returns).  Updates below
100% are removed.  The last ``100%`` line of each run is kept.

Author: Cursor / Grok 4.7.  Copyright ambiguous.
"""

import re

from docutils import nodes
from docutils.parsers.rst.directives import flag

from sphinx_autorun import RunBlock


# ``remote: Counting objects: 100% (10/10), done.``
_GIT_PROGRESS = re.compile(
    r'^.*:\s*(?P<pct>\d{1,3})%\s*\(\d+/\d+\).*$')

# ``100%  2.86 MiB        137 MiB/s 0s`` or a bare ``100%``.
_METER_PROGRESS = re.compile(
    r'^\s*(?P<pct>\d{1,3})%(?P<rest>\s.*)?$')

_METER_TOKEN = re.compile(
    r'^(?:'
    r'\d+(?:\.\d+)?'
    r'|[kKMGTPE]i?B(?:/s)?'
    r'|\d+s'
    r'|\d+:\d\d(?::\d\d)?'
    r'|\(\d+/\d+\),?'
    r'|done\.?'
    r'|\[[^\]]*\]'
    r'|[█▇▆▅▄▃▂▁░▒▓=\-#>|]+'
    r')$'
)


def _rest_is_meter(rest):
    tokens = [token.rstrip(',') for token in rest.split()]
    return bool(tokens) and all(_METER_TOKEN.match(token) for token in tokens)


def _progress_info(fragment, via_cr):
    """Return ``(percent, label)`` for one progress update, else None.

    *label* is the text before the percent.  A later line with the same label
    continues the same run, so ``Writing objects: 100% (3/3)`` is dropped when
    the next line is ``Writing objects: 100% (3/3), ... done.``
    """
    text = fragment.strip()
    if not text:
        return None
    match = _GIT_PROGRESS.match(text)
    if match is not None:
        percent = int(match.group('pct'))
        if not 0 <= percent <= 100:
            return None
        marker = match.group('pct') + '%'
        return percent, text[:text.rfind(marker)].strip()
    match = _METER_PROGRESS.match(text)
    if match is None:
        return None
    percent = int(match.group('pct'))
    if not 0 <= percent <= 100:
        return None
    rest = (match.group('rest') or '').strip()
    # A bare ``50%`` line is ordinary output.  Carriage-return redraws
    # and meter tails (sizes, rates, ``(n/n)``) are progress.
    if not via_cr and not (rest and _rest_is_meter(rest)):
        return None
    return percent, ''


def suppress_progress(text):
    """Remove partial percent updates, keeping the last 100% of each run.

    ``\\r\\n`` is a normal line break.  A lone ``\\r`` starts a redraw of the
    same line, which is how git-annex and git print a meter.  A run ends when
    the percent decreases, the label before the percent changes, or a
    non-progress line appears.  Whitespace used to erase a meter is discarded
    with the partial updates.  Of the ``100%`` lines in a run, only the last
    is kept, which drops a bare ``100% (n/n)`` line duplicated by the following
    ``100% (n/n), ... done.`` line.
    """
    normalized = text.replace('\r\n', '\n')
    parts = re.split(r'(\n|\r)', normalized)
    out = []
    sequence = []
    via_cr = False

    def flush_sequence():
        nonlocal sequence
        if not sequence:
            return
        hundreds = [line for percent, line, _label in sequence if percent == 100]
        sequence = []
        if not hundreds:
            return
        if out and not out[-1].endswith('\n'):
            out.append('\n')
        out.append(hundreds[-1])
        out.append('\n')

    index = 0
    while index < len(parts):
        fragment = parts[index]
        separator = parts[index + 1] if index + 1 < len(parts) else ''
        index += 2
        if fragment.strip() == '':
            # Spaces after ``\r`` erase the meter.  An empty piece between
            # ``\n`` and ``\r`` is only a split artifact.
            if via_cr or separator == '\r':
                via_cr = separator == '\r'
                continue
            flush_sequence()
            if separator == '\n':
                out.append('\n')
            via_cr = False
            continue
        info = _progress_info(fragment, via_cr)
        if info is not None:
            percent, label = info
            if sequence and (percent < sequence[-1][0] or label != sequence[-1][2]):
                flush_sequence()
            sequence.append((percent, fragment.strip(), label))
        else:
            flush_sequence()
            out.append(fragment)
            if separator == '\n':
                out.append('\n')
        via_cr = separator == '\r'
    flush_sequence()
    return ''.join(out)


class SuppressProgressRunBlock(RunBlock):
    """``runblock`` that can hide partial percent-progress lines."""

    option_spec = dict(RunBlock.option_spec)
    option_spec.update({
        'suppress-progress': flag,
        'no-suppress-progress': flag,
    })

    def _suppress_progress(self):
        if 'no-suppress-progress' in self.options:
            return False
        if 'suppress-progress' in self.options:
            return True
        env = self.state.document.settings.env
        return bool(getattr(env.config, 'autorun_suppress_progress', False))

    def run(self):
        rendered = super().run()
        if not self._suppress_progress():
            return rendered
        rewritten = []
        for node in rendered:
            if not isinstance(node, nodes.literal_block):
                rewritten.append(node)
                continue
            text = suppress_progress(node.rawsource)
            literal = nodes.literal_block(text, text)
            literal['language'] = node.get('language', '')
            literal['linenos'] = node.get('linenos', False)
            rewritten.append(literal)
        return rewritten


def _nb_progress_enabled(nb_renderer):
    renderer = getattr(nb_renderer, 'renderer', None)
    env = getattr(renderer, 'sphinx_env', None)
    config = getattr(env, 'config', None)
    return bool(getattr(config, 'autorun_suppress_progress', False))


def _filter_stream_output(nb_renderer, output):
    if not _nb_progress_enabled(nb_renderer):
        return output
    text = output['text']
    if not isinstance(text, str):
        text = ''.join(text)
    filtered = suppress_progress(text)
    if filtered == text:
        return output
    cloned = output.copy()
    cloned['text'] = filtered
    return cloned


def _install_notebook_filter():
    """Filter notebook stdout/stderr with the same progress rules."""
    from myst_nb.core.render import NbElementRenderer

    if getattr(NbElementRenderer.render_stdout, '_progress_wrapped', False):
        return
    orig_stdout = NbElementRenderer.render_stdout
    orig_stderr = NbElementRenderer.render_stderr

    def render_stdout(self, output, *args, **kwargs):
        return orig_stdout(self, _filter_stream_output(self, output), *args, **kwargs)

    def render_stderr(self, output, *args, **kwargs):
        return orig_stderr(self, _filter_stream_output(self, output), *args, **kwargs)

    render_stdout._progress_wrapped = True
    render_stderr._progress_wrapped = True
    NbElementRenderer.render_stdout = render_stdout
    NbElementRenderer.render_stderr = render_stderr


def setup(app):
    app.add_config_value('autorun_suppress_progress', False, 'env')
    # Replace the stock directive.  override avoids a warning under
    # sphinx-build --fail-on-warning.
    app.add_directive('runblock', SuppressProgressRunBlock, override=True)
    _install_notebook_filter()
    return {'version': '1.0', 'parallel_read_safe': True}
