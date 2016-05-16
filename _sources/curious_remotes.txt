#######################################################
git remotes - working with other people, making backups
#######################################################

This page follows on from :doc:`curious_git`.

It covers git **remotes**.  Remotes are links to other git repositories.

Now you are keeping the history of your data with git, you also want to make
sure you have a backup in case your current computer dies.

You might want to work with a colleague on the same project.  Perhaps your
colleague Anne is working on the same files, and you want to merge her changes
into yours.

We use git "remotes" to solve both of these problems.
Commands for working with remotes are:

* ``git remote`` |--| for adding and editing remotes;
* ``git clone`` |--| make a new copy of a repository, and make a remote
  that points to the original repository;
* ``git fetch`` |--| update stored information about a rempote repository;
* ``git push`` |--| upload information from this repository to a remote
  repository;
* ``git pull`` |--| a command combining ``git fetch`` and ``git merge``.  The
  command first fetches information from the remote repository, then merges
  the current state of a remote branch with a local branch.

Keeping backups with remotes
============================

Let's say you have an external backup disk and you want to record all the
history of your work on the backup disk.

To do this you need three steps:

* Make an empty backup repository on the external backup disk;
* Point your current git repository at the backup repository with ``git remote
  add``;
* Send the changes to the backup repository with ``git push``.

We will start with the repository that we made during :doc:`curious_git`.

Make the empty backup repository
--------------------------------

.. workvar:: usb_mountpoint
    :var_type: render

    echo "/Volumes/my_usb_disk"

.. workvar:: usb_mountpoint
    :var_type: run
    :omit_link:

    rm -rf repos
    mkdir repos
    echo "$PWD/repos"

Let's say your external disk is mounted at |usb_mountpoint|.

We make a new empty repository:

.. desktoprun::

    git init --bare {{ usb_mountpoint }}/nobel_prize.git

Notice the ``--bare`` flag.  This tells git to make a repository that does not
have a working tree, but only the ``.git`` repository directory:

.. desktoprun::

    ls {{ usb_mountpoint }}/nobel_prize.git

This is what we want in this case, because we will not ever want to edit the
files in the |usb_mountpoint| backup repository, we will only be editing files
in our local ``nobel_prize`` directory, committing those changes locally (as
we have done above), and then "pushing" these changes to the backup repository
[#bare-detail]_.

Tell the current git repository about the backup repository
-----------------------------------------------------------

Check we're in our local git repository:

.. prizerun::

    pwd

Add a remote.  A remote is a link to another repository.

.. prizerun::

    git remote add usb_backup {{ usb_mountpoint }}/nobel_prize.git

List the remotes:

.. prizerun::

    git remote -v

The list shows that we can both ``fetch`` and ``push`` to this repository, of
which more later.

Git has written the information about the remote URL to the repository config
file |--| ``.git/config``:

.. prizerun::

    cat .git/config

git push |--| push all data for a local branch to the remote
------------------------------------------------------------

We now want to synchronize the data in our ``nobel_prize`` repository with the
remote ``usb_backup``.  The command to do this is ``git push``.

Before we do the push, there are no objects in the ``.git/objects`` directory
of the ``usb_backup`` backup repository:

.. desktoprun::

    ls {{ usb_mountpoint }}/nobel_prize.git/objects

Then we push:

.. prizerun::

    git push usb_backup master

This command tells git to take all the information necessary to reconstruct
the history of the ``master`` branch, and send it to the remote repository.
Sure enough, we now have files in ``.git/objects`` of the backup repository:

.. desktoprun::

    ls {{ usb_mountpoint }}/nobel_prize.git/objects

You'll see that the 'master' branch in the backup repository now points to the
same commit as the master branch in the local repository:

.. prizerun::

    cat .git/refs/heads/master

.. desktoprun::

    cat {{ usb_mountpoint }}/nobel_prize.git/refs/heads/master

The local repository has a copy of the last known position of the master
branch in the remote repository.

.. prizerun::

    cat .git/refs/remotes/usb_backup/master

You can see the last known positions of the remote branches using the ``-r``
flag to ``git branch``:

.. prizerun::

    git branch -r  -v

To see both local and remote branches, use the ``-a`` flag:

.. prizerun::

    git branch -a  -v

.. _git-push:

git push |--| synchronizing repositories
----------------------------------------

``git push`` is an excellent way to do backups, because it only transfers the
information that the remote repository does not have.

Let's see that in action.

First we make a new commit in the local repository, with the following
changes:

.. prizerun::
    :hide:

    cat << EOF >> nobel_prize.md

    = More notes for the discussion

    TODO: express greater confidence in the results.
    EOF

.. prizerun::

    git diff

.. prizecommit:: buffing 2012-04-11 15:13:13

    git add nobel_prize.md
    git commit -m "Buff up the paper some more"

Git updated the local ``master`` branch, but the remote does not know about
this update yet:

.. prizerun::

    git branch -a -v

We already know there will be three new objects in ``.git/objects`` after this
commit.  These are:

* a new blob (file) object for the modified ``nobel_prize.md``;
* a new tree (directory listing) object associating the new hash for the
  contents of ``nobel_prize.md`` with the ``nobel_prize.md``
  filename;
* the new commit object.

Usually we don't need to worry about which objects these are, but here we will
track these down to show how ``git push`` works.

The commit object we can see from the top of ``git log``.  I've used the
``-1`` flag to show only the first entry in the log:

.. prizerun::

    git log -1

So the commit is |buffing|. We can get the tree object from the commit
object:

.. prizerun::

    git cat-file -p {{ buffing }}

We can show the tree object contents to get the object for the new
version of ``nobel_prize.md``:

.. depends on history

.. prizevar:: sha_fname

    echo "function sha_fname { echo \${1:0:2}/\${1:2}; }; sha_fname "

.. prizevar:: buffing-fname

    {{ sha_fname }} {{ buffing }}

.. prizevar:: buffing-tree

    git rev-parse {{ buffing }}:./

.. prizevar:: buffing-tree-fname

    {{ sha_fname }} {{ buffing-tree }}

.. prizerun::

    git cat-file -p {{ buffing-tree }}

.. prizevar:: buffing-paper-obj

    git rev-parse {{ buffing }}:nobel_prize.md

.. prizevar:: buffing-paper-obj-fname

    {{ sha_fname }} {{ buffing-paper-obj }}

We do have these objects in the local repository:

.. prizerun::

    ls .git/objects/{{ buffing-fname }}
    ls .git/objects/{{ buffing-tree-fname }}
    ls .git/objects/{{ buffing-paper-obj-fname }}

|--| but we don't have these objects in the remote repository yet (we haven't
done a ``push``):

.. prizerun::
    :allow-fail:

    REMOTE_OBJECTS={{ usb_mountpoint }}/nobel_prize.git/objects
    ls $REMOTE_OBJECTS/{{ buffing-fname }}
    ls $REMOTE_OBJECTS/{{ buffing-tree-fname }}
    ls $REMOTE_OBJECTS/{{ buffing-paper-obj-fname }}

Now we do a push:

.. prizerun::

    git push usb_backup master

The branches are synchronized again:

.. prizerun::

    git branch -a -v

We do have the new objects in the remote repository:

.. prizerun::

    REMOTE_OBJECTS={{ usb_mountpoint }}/nobel_prize.git/objects
    ls $REMOTE_OBJECTS/{{ buffing-fname }}
    ls $REMOTE_OBJECTS/{{ buffing-tree-fname }}
    ls $REMOTE_OBJECTS/{{ buffing-paper-obj-fname }}

You might also be able to see how git would work out what to transfer.  See
:doc:`git_push_algorithm` for how it could work in general, and for this case.

git clone |--| make a fresh new copy of the repo
------------------------------------------------

Imagine we have so far been working on our trusty work desktop.

We unplug the external hard drive, put it in our trusty bag, and take the
trusty bus back to our trusty house.

Now we want to start work on the paper.

We plug the hard drive into the laptop, it gets mounted again at
|usb_mountpoint|.

This time we want a repository with a working tree.

The command we want is ``git clone``:

.. laptoprun::

    git clone {{ usb_mountpoint }}/nobel_prize.git

.. note::

    You'll see that the shell prompt has changed from ``[desktop]$`` to
    ``[laptop]$``.  I used these prompts to make it more obvious which machine
    we are working on.

We have a full backup of the repository, including all the history:

.. laptoprun::

    cd nobel_prize
    git log --oneline --graph

git made a ``remote`` automatically for us, because it recorded where we
cloned from.  The default name for a git remote is ``origin``:

.. prizelaprun::

    git remote -v

Of course, just after the clone, the remote and the local copy are
synchronized:

.. prizelaprun::

    git branch -a -v

Now we could make some edits:

.. prizelaprun::
    :hide:

    echo "The brain is a really big network." >> nobel_prize.md

.. prizelaprun::

    git diff

Then we do an add and commit:

.. prizelapcommit:: wine-ideas 2012-04-11 20:13:31

    git add nobel_prize.md
    git commit -m "More great ideas after some wine"

The local copy is now ahead of the remote:

.. prizelaprun::

    git branch -a -v

At the end of the night's work, we push back to the remote on the USB disk:

.. prizelaprun::

    git push origin master

The local and remote are synchronized again:

.. prizelaprun::

    git branch -a -v

git fetch |--| get all data from a remote
-----------------------------------------

``git fetch`` fetches data from a remote repository into a local one.

Now we are back at the work desktop.  We don't have the great ideas from last
night in the local repository.  Here is the latest commit in the work desktop
repository:

.. prizerun::

    git log -1

Here are the branch positions in the work desktop repository:

.. prizerun::

    git branch -a -v

As you can see, the last known positions of the remote branches have not
changed from last night.  This reminds us that the last known positions only
get refreshed when we do an explicit git command to communicate with the
remote copy.  Git stores the "last known positions" in ``refs/remotes``.  For
example, if the remote name is ``usb_backup`` and the branch is ``master``,
then the last known position (commit hash) is the contents of the file
``refs/remotes/usb_backup/master``:

.. prizerun::

    cat .git/refs/remotes/usb_backup/master

The commands that update the last known positions are:

* ``git clone`` (a whole new copy, copying the remote branch positions with
  it);
* ``git push`` (copies data and branch positions to the remote repository, and
  updates last known positions in the local repository);
* ``git fetch`` (this section) (copies data and last known positions from
  remote repository into the local repository);
* ``git pull`` (this is nothing but a ``git fetch`` followed by a ``git
  merge``).

Now we have plugged in the USB drive, we can fetch the data and last known
positions from the remote:

.. prizerun::

    git fetch usb_backup

The last known positions are now the same as those on the remote repository:

.. prizerun::

    git branch -a -v

We can set our local master branch to be the same as the remote master branch
by doing a merge:

.. prizerun::

    git merge usb_backup/master

This does a merge between ``usb_backup/master`` and local ``master``.  In this
case, the "merge" is very straightforward, because there have been no new
changes in local ``master`` since the new edits we have in the remote.
Therefore the "merge" only involves setting local ``master`` to point to the
same commit as ``usb_backup/master``.  This is called a "fast-forward" merge,
because it only involves advancing the branch pointer, rather than fusing two
lines of development with a merge commit:

.. prizerun::

    git log --oneline --graph

git pull |--| git fetch followed by git merge
---------------------------------------------

``git pull`` is a shortcut for ``git fetch`` followed by ``git merge``.

For example, instead of doing ``git fetch usb_backup`` and ``git merge
usb_backup/master`` above, we could have done ``git pull usb_backup master``.
If we do that now, of course there is nothing to do:

.. prizerun::

    git pull usb_backup master

When you first start using git, I strongly recommend you always use an
explicit ``git fetch`` followed by ``git merge`` instead of ``git pull``.  It
is very common to run into problems using ``git pull`` that are made more
confusing by the fusion of the "fetch" and "merge" step.  For example, it is
not uncommon that you have done more work on a local copy, before you do an
innocent ``git pull`` from a repository with new work on the same file.  You
may well get merge conflicts, which can be rather surprising and confusing,
even for experienced users.  If you do ``git fetch`` followed by ``git
merge``, the steps are clearer so the merge conflict is less confusing and it
is clearer what to do.

Linking local and remote branches
---------------------------------

It can get a bit boring typing all of::

    git push usb_backup master

It may well be that we nearly always want to ``git push`` the ``master``
branch to ``usb_backup master``.

We can set this up using the ``--set-upstream`` flag to ``git push``.

.. prizerun::

    git push usb_backup master --set-upstream

Git then records this association in the ``.git/config`` file of the
repository:

.. prizerun::

    cat .git/config

We add some edits:

.. prizerun::
    :hide:

    echo "Is the network comment too obvious?" >> nobel_prize.md

.. prizerun::

    git diff

.. prizecommit:: no-network 2012-04-12 11:13:13

    git add nobel_prize.md
    git commit -m "Rethinking the drinking again"

Now instead of ``git push usb_backup master`` we can just do ``git push``.

Before we try this, we need to set a default configuration variable to avoid a
confusing warning. See ``git config --help`` for more detail:

.. prizerun::

    git config push.default simple

.. prizerun::

    git push

Notice that git didn't need to as where to "push" to.

Git also knows what to do if we do ``git fetch`` from this branch.

To show this in action, we go home to the laptop and fetch the desktop work
from the USB drive.

.. laptoprun::

    cd nobel_prize
    git fetch origin
    git merge origin/master

Then we do some more edits:

.. prizelaprun::
    :hide:

    echo "More convinced by networks." >> nobel_prize.md

.. prizelaprun::

    git diff

We add these edits as a new commit:

.. prizelapcommit:: convinced 2012-04-12 22:13:31

    git add nobel_prize.md
    git commit -m "I think better at home"

Then we push this commit back to the USB disk, setting the link between the
laptop branch and the remote for good measure:

.. prizelaprun::

    git push origin master --set-upstream

Back to the work desktop to demonstrate "fetch" after we have done ``git
push`` with ``--set-upstream`` above:

.. prizerun::

    git fetch

Notice that ``git fetch`` now knows where to "fetch" from.

We still need to do an explicit merge:

.. prizerun::

    git merge usb_backup/master

Remotes in the interwebs
------------------------

So far we've only used remotes on the filesystem of the laptop and desktop.

Remotes can also refer to storage on |--| remote |--| machines, using
communication protocols such as the "git" protocol, ssh, http or https.

For example, here is the remote list for the repository containing this
tutorial:

.. workrun::

    git remote -v

Check out bitbucket_ and github_ for free hosting of your repositories.  Both
services offer free hosting of data that anyone can read (public
repositories).  Bitbucket offers free hosting of private repositories, and
Github will host some private repositories for education users.

.. rubric:: Footnotes

.. [#bare-detail] The reason we need a bare repository for our backup goes
   deeper than the fact we do not need a working tree.  We are soon going to
   do a ``push`` to this backup repository.  The ``push`` has the effect of
   resetting the position of a branch (usually ``master``) in the backup repo.
   Git is very reluctant to set a branch position in a remote repository with
   a working tree, because the new branch position will not not match the
   existing content of the working tree.  Git could either leave the remote
   working tree out of sync with the new branch position, or update the remote
   working tree by doing a checkout of the new branch position, but either
   thing would be very confusing for someone trying to use the working tree in
   that repository.  So, by default git will refuse to ``push`` a new branch
   position to a remote repository with a working tree, giving you a long
   explanation as to why it is refusing, and listing things you can do about
   it.  You can force git to go ahead and do the push, but it is much safer to
   use a bare repository.

.. include:: links_names.inc
.. include:: working/object_names.inc
