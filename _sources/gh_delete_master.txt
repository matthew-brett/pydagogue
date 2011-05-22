###########################
Deleting your master branch
###########################

You've forked some project on github.

You clone your fork.

Now you've got a ``master`` branch.  It's the ``master`` branch of your fork.

It can be tempting to do work in the master branch and ask for a pull request.

That is best avoided because:

* It's natural to carry on working in your ``master`` and that will pollute your
  pull request with other commits
* ``master`` is not a descriptive name for a set of changes.  It's easier for
  the person reviewing your code to have something like ``fix-for-issue-12``.
* You may well also have a tracking branch pointing to the main upstream repo.
  You might call that something like ``upstream-master``.  It's easy to lose
  concentration and forget you are on ``upstream-master`` instead of your
  ``master``, and nasty errors can result.

To avoid this, I delete the ``master`` branch from my forked copy.  However, to
make that work, you have to tell github_ not to monitor your ``master`` branch.

********************
How to delete master
********************

First you delete ``master`` in your local clone. To do this we first make a new
branch called ``placeholder`` or similar, and delete ``master`` from there::

    git branch placeholder
    git checkout placeholder
    git branch -D master

All good so far.  We next want to delete the branch on github.  However, if we
do this the naive way::

    git push origin :master

we just get an error like this::

    remote: error: refusing to delete the current branch: refs/heads/master
    To git@github.com:matthew-brett/datarray.git
    ! [remote rejected] master (deletion of the current branch prohibited)
    error: failed to push some refs to 'git@github.com:matthew-brett/datarray.git'

That is because github is looking at the ``master`` branch to provide the web
content when you browse that repository.  So we first have to make github look
at our ``placeholder`` branch instead, then delete ``master``.

First push up the ``placeholder`` branch::

    git checkout placeholder # if not on placeholder already
    git push origin placeholder

Then set ``placeholder`` to be the github default branch.  Go to the main github
page for your forked repository, and click on the "Admin" button.

There's a "Default branch" dropdown list near the top of the screen.  From
there, select ``placeholder``.  On the interface I'm looking at, a green tick
appears above the dropdown list.  Now you can do (from the command line)::

    git push origin :master

and - no master branch...
