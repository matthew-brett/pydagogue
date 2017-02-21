.. _git-diff-dots:

############################
Two and three dots with diff
############################

.. note::

   Remember it's different for ``git log`` - see :ref:`git-log-dots` and
   :ref:`pain-in-dots`

*****************
Diff without dots
*****************

Two dots is the default in ``git diff``.  That is, if you do::

    git diff master topic

what you'll get is the same as if you asked for::

    git diff master..topic

So ``git diff`` without dots is the same as :ref:`git-diff-two-dots`.

.. _git-diff-two-dots:

******************
Diff with two dots
******************

Imagine a series of commits A, B, C, D...  Imagine that there are two
branches, *topic* and *master*.  You branched *topic* off *master* when
*master* was at commit 'E'.  The graph of the commits looks like this::

          A---B---C topic
         /
    D---E---F---G master

Then::

    git diff master..topic

will output the difference from G to C (i.e. with effects of F and G).

********************
Diff with three dots
********************

Using the three-dot form::

    git diff master...topic

This shows the differences between ``master`` and ``topic`` *starting at the
last common commit*.

In this case therefore it would output just differences in the ``topic`` branch
(i.e. only A, B, and C).  [#thank_yarik]_

.. rubric:: Footnotes

.. [#thank_yarik] Thanks to Yarik Halchenko for this explanation.
