.. _vim-mergetool:

###############################
Using vim as a mergetool in git
###############################

Setup::

    git config --global merge.tool gvimdiff
    git config --global mergetool prompt false
    git config --global merge.conflictstyle diff3

The last is so that we can see the base revision displayed within the merge
markers, in the merged file.  The *base* the revision that was the most recent
common basis for the two different versions implied in the merge.

Rebasing::

    git rebase main-master
    git mergetool

Quoting from ``git mergetool --help``:

    When git mergetool is invoked with this tool (either through the -t or
    --tool option or the merge.tool configuration variable) the configured
    command line will be invoked with $BASE set to the name of a temporary file
    containing the common base for the merge, if available; $LOCAL set to the
    name of a temporary file containing the contents of the file on the current
    branch; $REMOTE set to the name of a temporary file containing the contents
    of the file to be merged, and $MERGED set to the name of the file to which
    the merge tool should write the result of the merge resolution.

Interpreting the text above in the context of ``git rebase --help`` - the
"current branch" will, in this case, be ``main-master`` - more generally it will
be the "upstream" branch in the rebase command line, or "newbase" if you used
the ``--onto <newbase>`` option.

On my screen, there are four windows, three at the top, and one below.  (This is
for git 1.7.4.1.  Versions at least until 1.7.2 had three windows, vertically
arranged, being LOCAL, MERGED and REMOTE in the terms below).  In a rebase, the
ones at the top will be

* LOCAL : the current branch (``git branch``). In the case of a rebase this will
  be the upstream branch (or <newbase> from ``--onto``).  Here it would be
  ``main-master``.
* BASE : the common basis against which LOCAL and REMOTE have changed. This
  allows us to see what LOCAL and REMOTE have changed against.
* REMOTE : the file as for the changes we are adding with the rebase.  In our
  case, that would be the branch we were on when we issued ``git rebase
  main-master``.

The one at the bottom is:

* MERGED : the file to which we write the changes, to be selected from LOCAL
  (new changes) REMOTE (upstream changes).  This is the file with the merge
  markers in it. If you have *conflictstyle* above set to ``diff3`` you will see
  the LOCAL, REMOTE and BASE versions within the mergemarker block.

Now, time to go through the lower pane, pulling in changes from the "upstream"
(left) pane, or the "rebase changes" (right) pane, as in one of::

    :diffg LO
    :diffg BA
    :diffg RE


