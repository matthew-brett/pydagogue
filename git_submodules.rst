###########################
How do git submodules work?
###########################

Git submodules can be a little confusing.

This page explains how git *stores* submodules.  My hope is that this will make
it easier to understand how to *use* submodules.

If you've read :doc:`curious_git` you will recognize this way of thinking.

***************
Why submodules?
***************

Submodules are useful when you have a project that is under git version
control, and you need files from another project that is also under git
version control.

**************
Worked example
**************

We will call the project that we need to use just *myproject*, and the project
that is using *myproject* we will call *super*.

We are expecting that "myproject" will continue to develop.

"Super" is going to start using some version of "myproject".  In the spirit of
version control, we want to keep track of exactly which "myproject" version
"super" is using.

``myproject``
=============

We make a little "myproject" to start:

.. workrun::
    :hide:

    rm -rf myproject
    rm -rf super
    rm -rf super-cloned

.. workrun::

    mkdir myproject
    cd myproject
    git init

.. projectcommit:: proj-init 2012-05-01 11:13:13

    echo "Important code and data" > some_data.txt
    git add some_data.txt
    git commit -m "Initial commit on myproject"

Back to the working directory containing the repositories:

.. workrun::

    cd ..

``super``
=========

Now a "super" project:

.. workrun::

    mkdir super
    cd super

Remember (from :doc:`curious_git`) that doing ``git add`` on a file adds a new
copy of that file to the ``.git/objects`` directory.  So, ``.git/objects``
starts off empty:

.. superrun::

    git init

.. superrun::

    tree -a .git/objects

When we ``git add`` a file, there is one new file in ``.git/objects``:

.. superrun::

    echo "This project will use ``myproject``" > README.txt
    git add README.txt

.. superrun::

    tree -a .git/objects

Now do the first commit for "super":

.. supercommit:: super-init 2012-05-01 12:12:12

    git commit -m "Initial commit on super"

The commit made two new objects in the ``.git/objects`` directory:

* a *tree* object giving the directory listing of the root directory;
* a *commit* object giving information about the commit itself.

So, we now have three files in ``.git/objects``:

.. superrun::

    tree -a .git/objects

Adding ``myproject`` as a submodule of ``super``
================================================

We use a git submodule to put "myproject" inside "super".  We will use the
name "subproject" for the submodule copy of "myproject", to make clear that it
is the submodule copy:

.. superrun::

    git submodule add ../myproject subproject

What just happened?:

.. superrun::

    git status

Notice that ``git submodule`` has already staged its changes, so we need the
``--staged`` flag to ``git diff`` to see what has changed:

.. superrun::

    git diff --staged

As you saw, the output from ``git submodule`` says ``Cloning into
subproject``, and sure enough, if we look in the new ``subproject`` directory,
there is a clone of "myproject" there:

.. superrun::

    tree -a subproject

So, ``git submodule`` has:

#. cloned "myproject" to "super" subdirectory "subproject";
#. created and staged a small text file called ``.gitmodules`` that records
   the relationship of the ``subproject`` subdirectory to the original
   "myproject" repository;
#. claimed to have made a new *file* in the "super" repository that records
   the "myproject" commit that the submodule contains.

It's the last of these three that is a little strange, so we will explore.

Storing the current commit of ``myproject``
===========================================

Why do I say that git "claims" to have made a new file to record the
"myproject" commit?

Remember that we had three files in the ``.git/objects`` directory of "super"
after the first commit.  After ``git submodule add`` we have four:

.. superrun::

    tree -a .git/objects

The new object is for the ``.gitmodules`` text file. I could work out which
object that is by comparing with the previous listing for ``.git/objects``,
but I can get the hash git will use for ``.gitmodules`` with:

.. superrun::

    git hash-object .gitmodules

.. workvar:: gitmodules-object

    cd super
    git hash-object .gitmodules

.. superrun::

    git cat-file -p {{ gitmodules-object }}

If there is only one new object in ``.git/objects``, and that is for
``.gitmodules``, then there is no new git object corresponding to the
"myproject" repository.  What has in fact happened, is that git records the
commit for "myproject" in the directory listing, instead of recording the
``subproject`` directory as a subdirectory (tree object) or a file (blob
object).  That is a bit difficult to see at the moment, because the directory
listing is in the git staging area and not yet written into a tree object.  To
write the tree object, we do a commit:

.. supercommit:: add-module 2012-05-01 13:22:10

    git commit -m "Adding the submodule"

Here is the commit hash for the commit we just made:

.. superrun::

    git log -1

Here's the full data for the commit, including the hash for the root directory
tree object:

.. superrun::

    git cat-file -p  {{ add-module }}

.. workvar:: add-submodule-tree

    cd super
    git log -1 --format="%T"

Here's the full data for the root directory tree object for the commit:

.. superrun::

    git cat-file -p {{ add-submodule-tree }}

As you can see, the two real files |--| ``.gitmodules`` and ``README.txt``
|--| are listed as type ``blob``, with the hashes of their file contents. This
is the usual way git refers to a file in a directory listing (see
:doc:`curious_git`). The new entry for ``subproject`` is of type ``commit``.
The hash is the current commit of the "myproject" repository, in the
``subproject`` copy:

.. superrun::

    cd subproject
    git log

Updating submodules from their source repositories
==================================================

How do we keep the ``subproject`` copy of "myproject" up to date with the
original ``myproject`` repository?

We go back to the original "myproject" repository and make another commit:

.. superrun::

    cd ../myproject

.. projectcommit:: myproject-more-data 2012-05-01 13:33:21

    # Now in the original "myproject" directory
    echo "More data" > some_more_data.txt
    git add some_more_data.txt
    git commit -m "Add some more data"

.. projectrun::

    git branch -v

Of course "super" has not changed, because we haven't updated the submodule
clone:

.. projectrun::

    cd ../super

.. superrun::

    git status

The "subproject" directory is a full git repository clone of the original
"myproject".  Remember that ``git submodule add`` created the directory by
cloning. The "myproject" clone has a remote from the URL we gave to ``git
subproject``.

.. superrun::

    # We're in the "super" directory
    cd subproject
    # Now we're in the submodule clone of "myproject"
    git remote -v

We can do a ``fetch`` / ``merge`` to get the new commit:

.. subprojectrun::

    # This is the same as "git pull"
    git fetch origin
    git merge origin/master

Now what do we see in "super"?

.. subprojectrun::

    cd ..

.. superrun::

    # Now we are in the "super" directory
    git status

.. superrun::

    git diff

Git is not tracking the *contents* of the "subproject" directory, but the *git
state* of the directory.  In this case, all "super" sees is that the commit
has changed.

As when we added the submodule, a ``git add`` of the ``subproject`` directory,
has the effect of updating the commit that the "super" tree is pointing to
in the staging area, but adds no new files to ``.git/objects``:

.. superrun::

    ls .git/objects/*/*

.. superrun::

    git add subproject

.. superrun::

    ls .git/objects/*/*

So ``git add subproject`` makes no new objects, but it does change the
"myproject" commit hash that ``subproject`` points to.

If we do the commit, we can see the root tree listing now points to the new
commit of "myproject":

.. supercommit:: super-more-data 2012-05-01 13:44:32

    git commit -m "Update myproject with more data"

.. superrun::

    git cat-file -p HEAD

.. workvar:: super-more-data-tree

    cd super
    git log -1 --format="%T"

.. superrun::

    git cat-file -p {{ super-more-data-tree }}

Cloning a repository with submodules
====================================

What happens if we clone the "super" project?

.. superrun::

    cd ..

.. workrun::

    # In directory below "super"
    git clone super super-cloned

.. workrun::

    cd super-cloned
    ls

What is in the new ``subproject`` directory?

.. superclonedrun::

    tree -a subproject

Nothing.  When you ``git clone`` a project with submodules, git does not clone
the submodules.

Getting the submodule repository clone takes two steps.  These are:

* initialize with ``git submodule init``;
* clone with ``git submodule update``.

Initializing the submodule copies the repository submodule information in
``.gitmodules`` to the repository ``.git/config`` file.  Having this as a
separate step is useful when you want to use a different clone URL from the
one recorded in ``.gitmodules``. This might happen if you want to use a local
repository to clone from instead of a slower internet repository.  In this
case, you can do ``git submodule init``, edit ``.git/config``, and then do the
cloning with ``git submdoule update``.

Here's ``.git/config`` before the ``init`` step:

.. superclonedrun::

    # .git/config before submodule init
    cat .git/config

.. superclonedrun::

    git submodule init

``.git/config`` after the ``init``:

.. superclonedrun::

    # .git/config after submodule init
    cat .git/config

We have done ``init``, but not ``update``. The submodule directory is still
empty:

.. superclonedrun::

    tree -a subproject

To do the submodule clone, use ``git submodule update`` after ``git submodule
init``:

.. superclonedrun::

    git submodule update

If you are happy to clone from the clone URL recorded in ``.gitmodules``, then
you can do both ``init`` and ``update`` in one step with:

.. superclonedrun::

    git submodule update --init

.. include:: links_names.inc
