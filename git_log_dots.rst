.. _git-log-dots:

###########################
Two and three dots with log
###########################

.. note::

   Remember it's different for ``git diff`` - see :ref:`git-diff-dots` and
   :ref:`pain-in-dots`

.. _git-log-two-dots:

********************
Logging without dots
********************

Two dots is the default in ``git log``.  That is, if you do::

    git log master topic

what you'll get is the same as if you asked for::

    git log master..topic

So logging without dots is the same as :ref:`git-log-two-dots`.

.. _git-log-two-dots:

*********************
Logging with two dots
*********************

Let's say you asked for this::

    git log start-branch..end-branch

You will see a log of a series of commits. The commits will be all the commits
reachable from ``end-branch`` that are not reachable from ``start-branch``.

In fact, the two dot form of log is shorthand.  The ``git log`` line above is
shorthand for::

    git log ^start-branch end-branch

``end-branch`` above means |emdash| "show me all commits that can be
reached from ``end-branch``". ``^start-branch`` means |emdash| "excluding any
commits that can be reached from ``start-branch``".

.. note:: What does "reachable" mean?

    A commit, :math:`s`, can be **reached** from some commit, :math:`t`, if and
    only if there is a path from :math:`s` to :math:`t` along the ancestry graph
    of the commits.

    The ancestry graph is the directed acyclic graph of the history, where the
    nodes are the commits and the edges are directed backwards from nodes to
    their parents.

    Put more formally, a sequence of commits, :math:`v_0, v_1, ..., v_n`, forms
    a **path** between :math:`v_0` and :math:`v_n` if and only if
    :math:`v_{i-1}` is the parent of :math:`v_i` for :math:`i=1` to :math:`i=n`.
    A commit is also reachable from itself, so a commit sequence of length 1 is
    defined as forming a path.

Obviously ``git log start-branch..end-branch`` cannot include the commit
pointed to by ``start-branch`` because you can always reach ``start-branch``
from itself.

Let's say we have this history::

                  H--I--J  topicB
                 /
                 | E---F---G  topicA
                 |/
     A---B---C---D  master

.. comment - || to restore vim formatting

What would ``git log topicB..topicA`` show?  From ``topicA`` we can
reach ``G, F, E, D, C, B, A``.  From ``topicB`` we can reach ``J, I, H, D, C, B,
A``.  So, the commits reachable from ``topicA`` but not reachable from
``topicB`` are ``G, F, E``.

***********************
Logging with three dots
***********************

Now you ask for this::

    git log start-branch...end-branch

There are three dots between ``start-branch`` and ``end-branch``.  This three
dot version of the command finds all commits that are reachable from
``start-branch``, OR that are reachable from ``end-branch`` BUT that are NOT
reachable from both ``start-branch`` AND ``end-branch``.

Put another way, you will see all commits reachable from ``start-branch`` AND
all commits reachable from ``end-branch`` BUT excluding any commits reachable
from any common ancestor.  As the ``gitrevisions`` man page puts it, the three
dots command above is equivalent to::

    git log start-branch end-branch --not $(git merge-base --all start-branch end-branch)

Put another way, if :math:`S` is the set of all commits that can be reached from
``start-branch`` and :math:`E` is the set of all commits that can be reached
from ``end-branch`` then the commits returned from the three dot version of log
are:

.. math::

    (S \cup E) \setminus (S \cap E)

(:math:`X \setminus Y` denotes the set of members of :math:`X` that are not
in set :math:`Y`).

By example, from the history above, let's think about what would we get from::

    git log topicB...topicA

From ``topicA`` we can reach this set of commits |emdash| ``G, F, E, D, C, B,
A``.  From ``topicB`` we can reach ``J, I, H, D, C, B, A``.  That means that we
can reach ``D, C, B, A`` from both of ``topicA`` AND ``topicB``.  So the
returned commits would be ``G, F, E, J, I, H``.

.. include:: links_names.inc
