########################
What are git submodules?
########################

Git submodules can be a little confusing.

This page explains how git *stores* submodules.  My hope is that this will make
it easier to understand how to *use* submodules.

If you've read :doc:`curious_git` you will recognize this way of thinking.

Submodules are useful when you have a project that is under git version
control, and you need files from another project that is also under git
version control.

We will call the project that we need to use just *myproject*, and the project
that is using *myproject* we will call *super*.

We are expecting that "myproject" will continue to develop.

"Super" is going to start using some version of "myproject".  In the spirit of
version control, we want to keep track of exactly which "myproject" version
"super" is using.

We make a little "myproject" to start:

.. runblock::
    :hide:

    rm -rf myproject
    rm -rf super
    rm -rf super-cloned

.. runblock::

    mkdir myproject
    cd myproject

.. projectcommit:: proj-init 2012-05-01 11:13:13

    git init
    echo "Important code and data" > some_data.txt
    git add some_data.txt
    git commit -m "Initial commit on myproject"

.. runblock::

    cd ..

Now a "super" project:

.. runblock::

    mkdir super
    cd super

.. supercommit:: super-init 2012-05-01 12:12:12

    git init
    echo "This project will use ``myproject``" > README.txt
    git add README.txt
    git commit -m "Initial commit on super"

We know git well enough to know that there must be three files now in the git
objects directory |--| one each for the ``README.txt`` file, the root
directory listing and the commit:

.. superrun::

    tree -a .git/objects

We use a git submodule to put "myproject" inside "super".  We will give the
submodule copy of "myproject" a different name to make it clear which is the
submodule:

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
#. created and staged a text file called ``.gitmodules`` that records the
   relationship of the "subproject" subdirectory to the original "myproject"
   repository;
#. claimed to have made a new *file* in the "super" repository that records
   the "myproject" commit that the submodule contains.

It's the last of these three that is a little strange, so we will explore.

Why do I say that git "claims" to have made a new file to record the
"myproject" commit?

Remember that we had three files in ``.git/objects`` after the first commit.
After ``git submodule add`` we have four:

.. superrun::

    tree -a .git/objects

The new object is for the ``.gitmodules`` text file. I could work out which
object that is by comparing with the previous listing for ``.git/objects``,
but I can get the hash git will use for ``.gitmodules`` with:

.. superrun::

    git hash-object .gitmodules

So |--| there is no new git object corresponding to the "myproject"
repository.  What has in fact happened, is that git records the commit for
"myproject" in the directory listing, instead of recording the ``subproject``
directory as a |--| directory.  That is a bit difficult to see at the moment,
because the directory listing is in the git staging area and not yet written
into a tree object.  To write the tree object, we do a commit:

.. supercommit:: add-module 2012-05-01 13:22:10

    git commit -m "Adding the submodule"

We're expecting to have six objects in ``.git/objects`` now |--| the three
objects for the first commit, the object for ``.gitmodules``, and a new tree
and commit object for the latest commit:

.. superrun::

    tree -a .git/objects

Now we can list the root directory tree. I can get this tree object by listing
the commit object with ``git cat-file``:

.. superrun::

    git cat-file -p HEAD

.. cmdaddvar:: add-module-tree

    cd super
    git log -1 --format="%T"

.. superrun::

    git cat-file -p {{ add-module-tree }}

As you can see, the two files |--| ``.gitmodules`` and ``README.txt`` |--| are
listed as type ``blob``. The new directory |--| ``subproject`` |--| is of type
``commit``.  The hash is the current commit of the "myproject" repository:

.. superrun::

    cd subproject
    git log

What happens if we change the contents of "myproject" in "super"?

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

If we ``git-add`` the "subproject" directory, it has the effect of updating
the commit that the "super" tree is pointing to in the staging area, but, as
before, adds no new files to ``.git/objects``:

.. superrun::

    git add subproject

There are still only six objects in ``.git/objects``

.. superrun::

    tree -a .git/objects

If we do the commit, we can see the root tree listing now points to the new
commit of "myproject":

.. supercommit:: super-more-data 2012-05-01 13:44:32

    git commit -m "Update myproject with more data"

.. superrun::

    git cat-file -p HEAD

.. cmdaddvar:: super-more-data-tree

    cd super
    git log -1 --format="%T"

.. superrun::

    git cat-file -p {{ super-more-data-tree }}

What happens if we clone the "super" project?

.. superrun::

    cd ..

.. runblock::

    # In directory below "super"
    git clone super super-cloned

.. runblock::

    cd super-cloned
    ls

What is in the new ``subproject`` directory?

.. superclonedrun::

    ls subproject

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

.. superclonedrun::

    # .git/config before submodule init
    cat .git/config

.. superclonedrun::

    git submodule init

.. superclonedrun::

    # .git/config after submodule init
    cat .git/config

To do the submodule clone, use ``git submodule update`` after ``git submodule
init``:

.. superclonedrun::

    git submodule update

If you are happy to clone from the clone URL recorded in ``.gitmodules``, then
you can do both ``init`` and ``update`` in one step with:

.. superclonedrun::

    git submodule update --init

.. include:: links_names.inc
