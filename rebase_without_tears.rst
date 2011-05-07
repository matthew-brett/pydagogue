####################
Rebase without tears
####################

Tears of frustration.

************
The man page
************

I'm looking at the ``git-rebase`` man page now.  I guess I may not be alone in
finding it hard to understand, and easy to forget.  I have twice or three times
worked out how it worked, and then forgotten, and wished I had written something
down to explain it to myself.  Here is that explanation.

.. _actual-rebase:

******************
Your actual rebase
******************

I like to think of rebase in its full form, because the full form helps to
remind me of what it is doing.  Here's the full form of most rebase commands
[#to-root]_::

    git rebase --onto <graft-point> <starting-at> <ending-with>

I'm using different names from the ``git-rebase`` manpage - see
[#manpage-names]_.

The shorter forms use defaults for things you don't specify:

* If you don't specify ``--onto``, ``<graft-point>`` defaults to
  ``<starting-at>``
* If you don't specify an ``<ending-with>``, ``<ending-with>`` defaults to the
  current branch.

********************************
Which branch does rebase modify?
********************************

rebase modifies the ``<ending-with>`` branch.  If you don't specify
``<ending-with>`` it will modify the default for ``<ending-with>``, that is, the
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

    git checkout topic~3 # E
    git tag divergence-point
    git checkout topic

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

Yes, because because the meaning of ``<starting-at> <ending-with>`` above is to
collect the commits that you are going to apply.  The commits that you apply are
the commits shown by ``git log <starting-at>..<ending-with>``.  I took the
liberty of making a repository to match the history above.  Here is the result
of ``git log --oneline master..topic``, before the rebase::

    8de3e90 C
    9dcbae2 B
    cc3741a A

And of course that is the same as ``git log --oneline divergence-point..topic``.
So we could also do the rebase command with::

    git rebase --onto master master topic

And, in fact, if you don't specify the ``--onto`` option, then rebase assumes
you want to graft onto the ``<starting-at>`` position, so you could also do::

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
                  X--Y--Z other-branch

.. [#manpage-names] I'm using differnt names for the command options, compared
   to the ``git-rebase`` manpage.  The manpage uses:

   * ``<newbase>`` for my ``<graft-point>``
   * ``<upstream>`` for my ``<starting-at>``
   * ``<branch>`` for my ``<ending-with>``