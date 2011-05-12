####################
Rebase without tears
####################

*****************************************
What is this "rebase" of which you speak?
*****************************************

Actually it's a little difficult to explain.  It's the process of taking a
fragment of git change history, and rewriting that history as if it had begun at
a different commit.  It's easiest to explain by example, and there are some
examples later in this page.  See also the `Pro-Git chapter on rebasing
<http://progit.org/book/ch3-6.html>`_

***********************
The git-rebase man page
***********************

I'm looking at the ``git-rebase`` man page
<http://www.kernel.org/pub/software/scm/git/docs/git-rebase.html>`_ now.  I may
not be alone in finding it hard to understand, and easy to forget.  I have
twice or three times worked out how it worked, and then forgotten, and wished I
had written something down to explain it to myself.  Here is that explanation.

.. _actual-rebase:

******************
Your actual rebase
******************

I like to think of rebase in its full form, because the full form helps to
remind me of what it is doing.  Here's the full form of most rebase commands
[#to-root]_::

    git rebase --onto <graft-point> <starting-after> <ending-with>

I'm using different names from the ``git-rebase`` manpage - see
[#manpage-names]_.

The shorter forms use defaults for things you don't specify:

* If you don't specify ``--onto``, ``<graft-point>`` defaults to
  ``<starting-after>``
* If you don't specify an ``<ending-with>``, ``<ending-with>`` defaults to the
  current branch.

*************
Basic example
*************

Let's go through the man page examples.  Here's a history tree::

          A---B---C topic
         /
    D---E---F---G master

We want to take the novel contents of the ``topic`` branch (``A, B, C``) and
regraft it so that it starts at the ``master`` branch, like this::

                  A'--B'--C' topic
                 /
    D---E---F---G master

Let's do something to ease the explanation, and tag the divergence point ``E``
thus::

    git tag divergence-point topic~3 # E

Obviously that gives us::

         A---B---C topic
        /
        | F---G master
        |/
    D---E  (tag) divergence-point

Reading the :ref:`actual-rebase` command, we suspect the command we want is::

   git rebase --onto master divergence-point topic

And indeed, that does give us what we want.  However we had a to make a tag for
the divergence point, and that was a bit annoying. Can we get away without that?

Yes, because because the meaning of ``<starting-after> <ending-with>`` above is to
collect the commits that you are going to apply.  See :ref:`which-commits` for
an explanation.  In brief, the commits that you apply are the commits shown by
``git log <starting-after>..<ending-with>``.  I took the liberty of making a
repository to match the history above.  Here is the result of ``git log
--oneline master..topic``, before the rebase::

    8de3e90 C
    9dcbae2 B
    cc3741a A

And of course that is the same as ``git log --oneline divergence-point..topic``.
So we could also do the rebase command with::

    git rebase --onto master master topic

And, in fact, if you don't specify the ``--onto`` option, then rebase assumes
you want to graft onto the ``<starting-after>`` position, so you could also do::

    git rebase master topic

and in fact, if you don't specify the ``<ending-with>`` position, rebase assumes
that you want ``<ending-with>`` to be the state of the current branch, so you
could also do::

    git checkout topic # unless you are on ``topic`` already
    git rebase master

**************
Other examples
**************

Here is another example from the ``git-rebase`` man page.  We want to go from
this::

     o---o---o---o---o  master
          \
           o---o---o---o---o  next
                            \
                             o---o---o  topic

to this::

     o---o---o---o---o  master
         |            \
         |             o'--o'--o'  topic
          \
           o---o---o---o---o  next

How?   Let's check the :ref:`actual-rebase` command.  Maybe it is this::

    git rebase --onto master next topic

Yup, that's it!  You understand rebase!

Now we want to go from this::


                             H---I---J topicB
                            /
                   E---F---G  topicA
                  /
     A---B---C---D  master

to this::


                  H'--I'--J'  topicB
                 /
                 | E---F---G  topicA
                 |/
     A---B---C---D  master

We check the :ref:`actual-rebase` command.  Could it be this?::

    git rebase --onto master topicA topicB 

Could it be anything else?  Congratulations, you are now a rebase master.

.. _which-commits:

********************************
Which commits will rebase apply?
********************************

It will apply all the commits found by::

    git log <starting-after>..<ending-with>

Which commits are these?  These are the commits that are reachable from
``<ending-with>`` that are not reachable from ``<starting-after>``.  See
:ref:`git-log-two-dots`.

.. which-branch:

********************************
Which branch does rebase modify?
********************************

rebase modifies the ``<ending-with>`` branch.  If you don't specify
``<ending-with>`` it will modify the default for ``<ending-with>``, that is, the
current branch.

.. rubric:: Footnotes

.. [#to-root]  I've missed out the ``--interactive`` option, but that doesn't
   change the logic.  There is one more substantial variation of the
   :ref:`actual-rebase` command, using ``--root``.  This goes::

        git rebase --onto <graft-point> --root   <ending-with>

   I've put a couple of extra spaces between ``--root`` and ``<ending-with>`` to
   emphasise that ``--root`` is a flag, and ``<ending-with>`` is an argument
   with the same meaning as for the normal rebase command.

   If you do ``git checkout <ending-with>`` and then ``git log``, you'll see all
   the commits down to and including the first (root) commit of that branch.
   The root commit is a commit without a parent.  The ``--root`` version of the
   rebase commands then takes all the commits, from the root commit up until
   ``<ending-with>``, including the root commit, and grafts them onto
   ``<graft-point>``.

   Let's say you somehow have two detached histories in your repository::

       A--B--C--D master

       X--Y--Z other-branch

   The root of ``master`` is A, and the root of ``other-branch`` is X.  To
   attach these histories you could do::

       git rebase --onto master --root   other-branch

   resulting in::

       A--B--C--D master
                 \
                  X'--Y'--Z' other-branch

   It would be annoying to have to do the same operation without the ``--root``
   option, because you'd first have to find the root commit, apply the root
   commit, and then rebase the rest of the X-Y-Z history on top of that, rather
   like::

       git tag root-of-other-branch other-branch~2 # tags X commit
       git branch tmp-branch master # start rebase at master
       git checkout tmp-branch
       git cherry-pick root-of-other-branch # apply root commit
       git rebase --onto tmp-branch root-of-other-branch other-branch
       # You are now on the rebased other-branch
       git branch -D tmp-branch

.. [#manpage-names] I'm using different names for the command options, compared
   to the ``git-rebase`` manpage.  The manpage uses:

   * ``<newbase>`` for my ``<graft-point>``
   * ``<upstream>`` for my ``<starting-after>``
   * ``<branch>`` for my ``<ending-with>``
