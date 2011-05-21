.. _pain-in-dots:

################
Pain in the dots
################

git_ uses a two and three dot notation for ``git log`` and ``git diff``.

Unfortunately they mean different, and nearly opposite things, in the two cases.

See :ref:`git-log-dots` for the explanation of ``git log`` and dots.  See
:ref:`git-diff-dots` for the ``git diff`` explanation.

See `git log and git diff
<http://genomewiki.ucsc.edu/index.php/Getting_Started_With_Git#Git_Diff_and_Git_Log>`_
for an alterative explanation.

******************
The dot difference
******************

This is a summary.  You need the pages above to get the full picture.

Imagine this history::

          A---B---C topic
         /
    D---E---F---G master

Obviously ``A, B, C`` is the stuff unique to ``topic``, and ``F, G`` is the
stuff unique to ``master``.

``log`` and two dots gives you the stuff unique to the second named branch.
So::

    git log master..topic

will show you a log of commits ``C, B, A``.

``log`` and three dots shows you the stuff unique to the second named branch AND
the stuff unique to the first named branch, so::

    git log master...topic

shows you ``C, B, A`` and ``F, G``.

``diff`` on the other hand, means something different.  So ``diff`` and two
dots::

    git diff master..topic

shows you all stuff that differs between the state as of ``master`` and the
state as of ``topic``.  It will show you the difference between the effect of
``A, B, C`` and the effect of ``F, G``.  You can think of this as being the
difference between the stuff unique to ``topic`` and the stuff unique to
``master``.

``diff`` and three dots::

    git diff master...topic

shows you the stuff that differs between ``topic`` and the last common ancestor
of (``topic``, ``master``). In this example that ancestor is commit ``E``.  Thus
three dots for diff is the difference caused by the stuff unique to ``topic``.
