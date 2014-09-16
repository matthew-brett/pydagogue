.. check with make doctest

####################################
The curious coder's guide to ``git``
####################################

*****************
git - love - hate
*****************

I've used git now for a long time.  I think it's a true masterpiece of design,
I use it all day every day and I just can't imagine what it would be like not
to use it. So, no question, I *love* git.

As y'all may know, `Linus Torvalds wrote git from scratch
<http://git-scm.com/book/en/Getting-Started-A-Short-History-of-Git>`_.  He
loves it too.  `Here is Linus talking about git
<http://www.youtube.com/watch?v=MShbP3OpASA#t=2288>`_ in a question and answer
session:

    Actually I'm proud of git. I want to say this. The fact that I had to
    write git was accidental, but Linux, the design came from a great mind,
    and that great mind was not mine. I mean you have to give credit for the
    design of Linux to Kernighan and Ritchie and Thompson. I mean there's a
    reason I like Unix and I wanted to redo it. I do want to say that git is a
    design that is mine and unique, and I'm proud of the fact that I can damn
    well also do good design from scratch.

But - some people hate git.  Really *hate* it. They find it confusing and
error prone and it makes them angry.  Why are there such different views?

I think the reason some people hate git, is because they don't yet understand
it.  I reason I can say this without being patronizing is because I went
through something similar myself.

When I first started using git, I found it uncomfortable.  I could see it was
very powerful, but I sometimes got lost and stuck and had to Google for a set
of magic commands to get me out of trouble.  I once accidentally made a huge
mess of our project's main repository by running a command I didn't
understand. Git often made me feel stupid.  It felt like a prototype racecar
with a badly designed dashboard that was just about to blow an engine or a
tire and take me off the road.

Then, one day, I read the `git parable`_.  The git parable is a little story
about a developer trying to work out how to make a version control system.  It
gradually builds up from copying whole directories of files to something very
much like git.  I didn't understand it all right away, but as soon as I read
this page, the light-bulb went on - I got git.  I suddenly started to feel
comfortable.  I knew for sure I could work out why git worked the way it did.
I could see that it must be possible how to do complicated and powerful
things, and I could work out how to do them.

Reading the git parable took me about 45 minutes, but those 45 minutes changed
me from an unhappy git user to the man you see before you today, someone who
uses git often every day, but, happily, knowing that I have the right tool for
the job.

So, my experience tells me that to use git - yes *use* git - you need to spend
that 45 minutes to *understand* git.  You don't believe me, or you think that
I'm a strange kind of person not like you who probably likes writing their own
operating systems. Not so - the insight I'm describing comes up over and over.
From `understanding git conceptually
<http://www.sbf5.com/~cduan/technical/git>`_:

    When I first started using Git, I read plenty of tutorials, as well as the
    user manual. Though I picked up the basic usage patterns and commands, I
    never felt like I grasped what was going on “under the hood,” so to speak.
    Frequently this resulted in cryptic error messages, caused by my random
    guessing at the right command to use at a given time. These difficulties
    worsened as I began to need more advanced (and less well documented)
    features.

    When I first started using Git, I read plenty of tutorials, as well as the
    user manual. Though I picked up the basic usage patterns and commands, I
    never felt like I grasped what was going on “under the hood,” so to speak.
    Frequently this resulted in cryptic error messages, caused by my random
    guessing at the right command to use at a given time. These difficulties
    worsened as I began to need more advanced (and less well documented)
    features.

Here's a quote from the `pro git book <http://git-scm.com/book>`_ by Scott Chacon.
The git book is a standard reference that is hosted on the main git website.

    Chapter 9: Git Internals

    You may have skipped to this chapter from a previous chapter, or you may
    have gotten here after reading the rest of the book — in either case, this
    is where you’ll go over the inner workings and implementation of Git. I
    found that learning this information was fundamentally important to
    understanding how useful and powerful Git is, but others have argued to me
    that it can be confusing and unnecessarily complex for beginners. Thus,
    I’ve made this discussion the last chapter in the book so you could read
    it early or later in your learning process. I leave it up to you to
    decide.

So - have no truck with people who try and tell you that you can just use git
and that you don't need the `deep shit
<http://rogerdudler.github.io/git-guide>`_.  You *do* need the deep shit, but
the deep shit isn't that deep, and it will take you an hour of your time to get
it.  And then I'm betting that you'll see that the alchemist has succeeded at
last, and the shit finally turned into gold.

So - please - invest an hour of your life to understand this stuff.
Concentrate, go slowly, make sure you get it. In return for an hour of your
life, you will get many happy years for which git will appear in its true
form, both beautiful and useful.

*****************************************************
The one thing about git you really need to understand
*****************************************************

``git`` is not really a "Version Control System". It is better described
as a "Content Management System", that turns out to be really good for
version control.

I'll say that again.  Git is a content management system.  Or - to quote from
the `root page of the git manual <http://git-scm.com/docs/git.html>`_: "git -
the stupid content tracker".

**************************************
So git is a content manager - so what?
**************************************

To understand why git does what it does, we first need to think about what a
content manager should do, and why we would want one.

As in the `git parable`_ - we'll try and design our own, and then see what
``git`` has to say.

(To go through this a little more slowly, and with more jokes, you might also
try my  `git foundations
<http://matthew-brett.github.com/pydagogue/foundation.html>`__ page).

While we are designing our own content management system, we will do a lot of
stuff longhand, to show how things work.  When we get to git, we will find it
these tasks for us.

*******************
The story so far...
*******************

You are writing a breakthrough paper showing that you can entirely
explain the brain using random numbers. You've got the draft paper, and
the analysis script and a figure for the paper. These are all in a
directory modestly named ``nobel_prize``.

In this directory, you have the paper draft ``nobel_prize_paper.txt``, the
analysis script ``very_clever_analysis.py``, and a figure for the paper
``stunning_figure.png``.

You can get this ground-breaking paper by downloading and unzipping
:download:`nobel_prize_files.zip`.

.. runblock::
    :hide:

    # clean up old files from previous doc run
    rm -rf nobel_prize

.. runblock:: bash

    unzip -o nobel_prize_files.zip

Here's what we get in our ``nobel_prize`` directory:

.. runblock::

    ls nobel_prize

The dog ate my results
======================

You've been working on this paper for a while.

About 2 weeks ago, you were very excited with the results. You ran the script,
made the figure, and went to your advisor, Josephine. She was excited too. The
figure looks good! You get ready to publish in Science.

Today you finished cleaning up for the Science paper, and reran the analysis,
and it doesn't look that good anymore. You go to see Josephine. She says "It
used to look better than that". That's what you think too. But:

* **Did it really look better before?**
* If it did, **why does it look different now?**

Deja vu all over again
======================

Given you are so clever and you have worked out the brain, it's really
easy for you to leap in your time machine, and go back two weeks to
start again.

What are you going to do differently this time?

Make regular snapshots
======================

You decide to make your own content management system called
``fancy_backups``.

It's very simple.

Every time you finish doing some work on your paper, you make a snapshot
of the analysis directory.

The snapshot is just a copy of all the files in the directory, kept
somewhere safe.

You make a directory to store the snapshots called ``.fancy_backups``:

.. runblock:: bash

    cd nobel_prize

.. prizerun::

    mkdir .fancy_backups

Then you make a directory for the first backup:

.. prizerun::

    mkdir .fancy_backups/1
    mkdir .fancy_backups/1/files

And you copy the files there:

.. prizerun::

    cp * .fancy_backups/1/files

Reminding yourself of what you did
==================================

For good measure, you put a file in the snapshot directory to remind you when
you did the snapshot, and who did it, and what was new for this snapshot. Call
this file ``info.txt``.  So, we write something like this:

.. prizewrite::

    # file: .fancy_backups/1/info.txt
    Date: April 1 2012, 14.30
    Author: I. M. Awesome
    Notes: First backup of my amazing idea

Now you have these files in the ``nobel_prize`` directory:

.. prizerun::

    tree -a

Every time you do some work on the files, you back them up in the same
way. After a few days:

.. prizerun::

    # Append some text to nobel_prize_paper.txt
    echo "The charts are very impressive" >> nobel_prize_paper.txt
    # Make a new snapshot
    mkdir .fancy_backups/2
    mkdir .fancy_backups/2/files
    cp * .fancy_backups/2/files

We make a new ``info.txt`` file describing what is new in this snapshot:

.. prizewrite::

    # file: .fancy_backups/2/info.txt
    Date: April 1 2012, 18.03
    Author: I. M. Awesome
    Notes: Fruit of enormous thought

The next day we write a little more on our paper:

.. prizerun::

    # Append some more text to nobel_prize_paper.txt
    echo "The graphs are also compelling" >> nobel_prize_paper.txt
    # Make another shapshot
    mkdir .fancy_backups/3
    mkdir .fancy_backups/3/files
    cp * .fancy_backups/3/files

We add a description of these changes:

.. prizewrite::

    # file: .fancy_backups/3/info.txt
    Date: April 2 2012, 11.20
    Author: I. M. Awesome
    Notes: Now seeing things clearly

After three days of work we have three snapshots in our backup directory:

.. prizerun::

    tree -a

You keep doing this for another couple of days, until again the time comes to
talk to Josephine. By now you have 5 snapshots.

.. prizerun::
    :hide:

    # Now we just cheat, and copy the commits
    cp -r .fancy_backups/3 .fancy_backups/4
    cp -r .fancy_backups/3 .fancy_backups/5

The future has not changed. Josephine again thinks the results have
changed. But now - you can check.

You go back and look at ``.fancy_backups/1/stunning_figure.png``. It
does look different.

You go through all the ``.fancy_backups`` directories in order. It turns
out that the figure changes in ``.fancy_backups/4``.

You look in ``.fancy_backups/4/info.txt`` and it says::

    Date: April 4 2012, 01.40
    Author: I. M. Awesome
    Notes: I always get the best ideas after I have been drinking.

Aha. Then you go find the problem in
``fancy_backups/4/very_clever_analysis.py``.

You fix ``very_clever_analysis.py``.

You make a new snapshot ``.fancy_backups/6``.

.. prizerun::
    :hide:

    # Cheat again
    cp -r .fancy_backups/3 .fancy_backups/6

Back on track for a scientific breakthrough

Terminology breakout
====================

Here are some
`terms <https://www.kernel.org/pub/software/scm/git/docs/gitglossary.html>`__.

Working tree
    The files you are working on in the current directory (``nobel_prize``).
    The files ``very_clever_analysis.py``, ``nobel_prize_paper.txt``,
    ``stunning_figure.png`` are the files in your working tree.

Repository
    The directory containing information about the history of the files. Your
    directory ``.fancy_snapshot`` is the repository.

Commit
    A completed snapshot. For example, ``.fancy_backups/1`` contains one
    commit.

We'll use these terms to get used to them.

Breaking up work into chunks
============================

You did some edits to the paper ``nobel_prize_paper.txt`` to edit the
introduction.

You also had a good idea for the analysis, and did some edits to
``very_clever_analysis.py``.

You've got used to breaking each new *commit* (snapshot) up into little
bits of extra work, with their own comments in the ``info.txt``.

You want to make two commits from your changes:

1. a commit containing the changes to ``nobel_prize_paper.txt``, with comment
   "Changes to introduction";
2. Another commit containing the changes to ``very_clever_analysis.py``
   with comment "Crazy new analysis"

How can I do that?

The staging area
================

You adapt the workflow. Each time you do a commit, you copy the contents of
the commit to directory ``.fancy_backups/staging_area``. That will be the
default contents of your next commit.

.. prizerun::

    mkdir .fancy_backups/staging_area
    cp .fancy_backups/6/files/* .fancy_backups/staging_area
    ls .fancy_backups/staging_area

Now, you do your edits to ``nobel_prize_paper.txt``, and
``very_clever_analysis.py`` in your *working tree* (the ``nobel_prize``
directory). You want to make a new commit containing the changes to the paper
but not the changes to the script.  You get ready for the next commit with:

.. prizerun::

    cp nobel_prize_paper.txt .fancy_backups/staging_area

The staging area now contains all the files for the upcoming commit
(snapshot). The upcoming commit only has the changes in the paper.

You make the commit by making the usual directories, and copying the contents
of the staging area into the commit ``files`` directory:

.. prizerun::

    # Make commit directories
    mkdir .fancy_backups/7
    mkdir .fancy_backups/7/files
    # Copy contents of staging area into commit directory
    cp .fancy_backups/staging_area/* .fancy_backups/7/files

with message:

.. prizewrite::

    # file: .fancy_backups/7/info.txt
    Date: April 10 2012, 14.30
    Author: I. M. Awesome
    Notes: Changes to introduction

After we have done the commit this way, by coping the staging area to the
commit ``files`` directory, the staging area is identical to the contents of
the commit.  Now you are ready for the next commit, that adds the changes to
the analysis script.

.. prizerun::

    cp very_clever_analysis.py .fancy_backups/staging_area

The commit is now *staged* and ready to be saved.

.. prizerun::

    # Our commit procedure; same as last time with "8" instead of "7"
    mkdir .fancy_backups/8
    mkdir .fancy_backups/8/files
    cp .fancy_backups/staging_area/* .fancy_backups/8/files

The message is:

.. prizewrite::

    # file: .fancy_backups/8/info.txt
    Date: April 10 2012, 14.35
    Author: I. M. Awesome
    Notes: Crazy new analysis

Here is what you have in your ``.fancy_backups`` directory:

.. prizerun::

    tree -a .fancy_backups

Now the very difficult problem
==============================

Let's say that the figure ``stunning_figure.png`` is large.

Let's say it changes only once across our 8 commits, at commit 5.

What should we do to save disk space for ``.fancy_backups``?

************************************
Cryptographic hashes might be useful
************************************

This section describes "Crytographic hashes". These are the key to an
excellent way to store our snapshots.  Later we will see that they are central
to the way that git works.

See : `Wikipedia on hash
functions <http://en.wikipedia.org/wiki/Cryptographic_hash_function>`__.

A *hash* is the result of running a *hash function* over a block of
data. The hash is a fixed length string that is the *signature* of that
exact block of data.  One common hash function is called SHA1.  Let's run this
via the command line:

.. runblock::

    # Make a file with a single line of text
    echo "git is a rude word in UK English" > git_is_rude
    # Show the SHA1 hash
    shasum git_is_rude

Not too exciting so far. However, the rather magical nature of this string is
not yet apparent. This SHA1 hash is a *cryptographic* hash because

* the hash value is (almost) unique to this exact file contents, and
* it is (almost) impossible to find some other file contents with the same
  hash

In other words, there is no practical way for you to find another file with
different contents that will give the same hash.

For example, a tiny change in the string makes the hash completely different.
Here I've just added a full stop at the end:

.. runblock::

    echo "git is a rude word in UK English." > git_is_rude_stop
    shasum git_is_rude_stop

So, if you give me some data, and I calculate the SHA1 hash value, and it
comes out as ``30ad6c360a692c1fe66335bb00d00e0528346be5``, then I can be very
sure that the data you gave me was exactly the ASCII string "git is a rude
word in UK English".

A crazy idea - use hash values as file names
============================================

Make a new directory:

.. prizerun::

    mkdir .fancy_backups/objects

Calculate the hash value for the figure:

.. prizerun::

    shasum .fancy_backups/1/files/stunning_figure.png

Save the figure with the hash value as the file name:

.. prizerun::

    cp .fancy_backups/1/files/stunning_figure.png .fancy_backups/objects/aff88ecead2c7166770969a54dc855c8b91be864

Do the same for the other two files in the first commit.

.. prizerun::

    shasum .fancy_backups/1/files/nobel_prize_paper.txt
    shasum .fancy_backups/1/files/very_clever_analysis.py

.. prizerun::

    cp .fancy_backups/1/files/nobel_prize_paper.txt .fancy_backups/objects/3af8809ecb9c6dec33fc7e5ad330e384663f5a0d
    cp .fancy_backups/1/files/very_clever_analysis.py .fancy_backups/objects/e7f3ca9157fd7088b6a927a618e18d4bc4712fb6

We now have three new files in ``.fancy_backups/objects``, one corresponding
to each unique file *contents* we have hashed:

.. prizerun::

    tree -a .fancy_backups/objects

Making the directory listing
============================

The snapshot has three files.  We can think of the file has having *content*
(the bytes contained in the file) and a *filename*.  We have already stored
the contents in the object directory, but with a different filename, from the
hash of the contents.  To record the filenames, we need to make a directory
listing.

To do this, we can point the snapshot to the hash filename versions of the
files by making a *text directory listing* or *tree* listing:

.. prizewrite::

    # file: .fancy_backups/1/directory_list
    Filename                Hash value
    ========                ==========
    nobel_prize_paper.txt   3af8809ecb9c6dec33fc7e5ad330e384663f5a0d
    stunning_figure.png     aff88ecead2c7166770969a54dc855c8b91be864
    very_clever_analysis.py e7f3ca9157fd7088b6a927a618e18d4bc4712fb6

The next commit - saves space!
==============================

Now we work on the files from the second commit. These are the files in
``.fancy_backups/2/files``.

Remember that we only changed ``nobel_prize_paper.txt`` in this commit.

Do we need to copy ``nobel_prize_papar.txt`` or ``stunning_figure.png`` to the
objects directory again?

No - because they have not changed.  Because they have not changed, their hash
values have not changed.  Because their hash values have not changed, and
because the hash values are unique to the contents, we already have the files
we need in the ``objects`` directory.

Specifically, because ``.fancy_backups/2/stunning_figure.png`` is the same as
``.fancy_backups/1/stunning_figure.png`` we know that the hash is the same,
and the hash is the one we've already calculated,
``aff88ecead2c7166770969a54dc855c8b91be864``.  We already have a file
``.fancy_backups/objects/aff88ecead2c7166770969a54dc855c8b91be864``, and we
know, because the hash values are unique, that this file must contain the
exact contents of ``.fancy_backups/1/stunning_figure.png``, which is also the
exact contents of ``.fancy_backups/2/stunning_figure.png``.

So in general, if we do a hash on a file, and then we find a filename the same
as this hash in the objects directory, we already have that exact contents
backed up, and we don't need to do a copy.

Here are the hashes for the files in commit 2:

.. prizerun::

    shasum .fancy_backups/2/files/nobel_prize_paper.txt
    shasum .fancy_backups/2/files/stunning_figure.png
    shasum .fancy_backups/2/files/very_clever_analysis.py

We already have files ``aff88ecead2c7166770969a54dc855c8b91be864`` and
``e7f3ca9157fd7088b6a927a618e18d4bc4712fb6`` in ``.fancy_backups/objects``, so
the only file we need to copy is ``nobel_prize_paper.txt``:

.. prizerun::

    cp .fancy_backups/2/files/nobel_prize_paper.txt .fancy_backups/objects/90aa1015732676bf63d2d950714a1f11196875fc

Here then is our directory listing for commit 2:

.. prizewrite::

    # file: .fancy_backups/2/directory_list
    Filename                Hash value
    ========                ==========
    nobel_prize_paper.txt   90aa1015732676bf63d2d950714a1f11196875fc
    stunning_figure.png     aff88ecead2c7166770969a54dc855c8b91be864
    very_clever_analysis.py e7f3ca9157fd7088b6a927a618e18d4bc4712fb6

An even more crazy idea - hash the directory list
=================================================

The directory listing is just a text file.  We can store the directory listing
as we store the other files, by writing an object file with the file hash:

.. prizerun::

    shasum .fancy_backups/1/directory_list

.. prizerun::

    cp .fancy_backups/1/directory_list .fancy_backups/objects/b7c9cd682e7d4bf28b82e76fb2276608f49e16d5

And we can do the same for the second commit:

.. prizerun::

    shasum .fancy_backups/2/directory_list

.. prizerun::

    cp .fancy_backups/2/directory_list .fancy_backups/objects/4f379c649a596d2f9cc2cf5b91f4a67a3101b65e

Now - would I get the same hash for the directory listing if I had had a
different figure?

Even more crazy idea - make the whole commit into a text file
=============================================================

We've seen that we can make a directory listing that is unique for the whole
contents of the snapshot files (file contents and file names).  Therefore the
*hash* of the directory listing is also unique for the contents of the
snapshot files.  So, we can make a *commit file* that is the ``info.txt`` file
above, but now with the hash of the directory listing included.  Including the
directory listing means that this *commit file* is now also unique to the
contents of the snapshot.  The commit file for the first commit might look
something like this:

.. prizewrite::

    # file: .fancy_backups/1/commit
    Date: April 1 2012, 14.30
    Author: I. M. Awesome
    Notes: First backup of my amazing idea
    Tree: b7c9cd682e7d4bf28b82e76fb2276608f49e16d5

The commit file for the second commit might look like this:

.. prizewrite::

    # file: .fancy_backups/2/commit
    Date: April 1 2012, 18.03
    Author: I. M. Awesome
    Notes: Fruit of enormous thought
    Tree: 4f379c649a596d2f9cc2cf5b91f4a67a3101b65e

The commit is now just a text file, and I can hash this too:

.. prizerun::

    shasum .fancy_backups/1/commit
    shasum .fancy_backups/2/commit

.. prizerun::

    cp .fancy_backups/1/commit .fancy_backups/objects/012ad9f6c3a715516514e8821a71d891c4211f8f
    cp .fancy_backups/2/commit .fancy_backups/objects/d4c297c8b0c768647e0b3faa9308a40d0e3cb4ba

Would the commit hash value change if the figure changed?

So crazy it's actually git
==========================

Now look in ``.fancy_backups/objects``:

.. prizerun::

    tree -a .fancy_backups/objects

That's 3 file copies for the files from the first commit, 1 file copy from the
second commit, 2 directory listings (for first and second commit) and two
commit listings (for the first and second commit) = 8 hash objects.

Linking the commits
===================

Can we completely get rid of ``.fancy_backups/1``, ``.fancy_backups/2``
-----------------------------------------------------------------------

The reason for our commit names "1","2", "3" was so we know that commit "2"
comes after commit "1" and before commit "3". Now our commits have filenames
with arbitrary hashes, we can't tell the order from the name.

However, the commit hash does uniquely identify the commit.  For example, we
know that the file beginning '012ad9f' *completely defines the first commit*:

.. prizerun::

    cat .fancy_backups/objects/012ad9f6c3a715516514e8821a71d891c4211f8f

We can specify the order by adding the commit hash of the previous
(parent) commit into the current commit:

.. prizewrite::

    # file: .fancy_backups/2/info.txt
    Date: April 1 2012, 18.03
    Author: I. M. Awesome
    Notes: Fruit of enormous thought
    Tree: 1dca3837b1076cdcfb02e86018377725e5d0e86e
    Parent: 012ad9f6c3a715516514e8821a71d891c4211f8f

Now we have the order of the commits from the links between them, where the
links are given by the hash value in the ``Parent`` field.

And now you are already a git master.

Gitting going (sorry)
^^^^^^^^^^^^^^^^^^^^^

**Note**: Much of the rest of this presentation comes from Fernando
Perez' excellent git tutorial in his `reproducible software
repository <https://github.com/fperez/reprosw>`__. Thanks to Fernando
for sharing.

We need to tell git about us before we start. This stuff will go into
the commit information.

.. prizerun::

    git config --global user.name "Matthew Brett"
    git config --global user.email "matthew.brett@gmail.com"

git often needs to call up a text editor. Choose the editor you like here::

    # Put here your preferred editor
    git config --global core.editor gedit

We also turn on the use of color, which is very helpful in making the
output of git easier to read::

    git config --global color.ui "auto"

Getting help
============

.. prizerun::

    git

Try ``git help add`` for an example.

Initializing the repository
===========================

We first set this ``nobel_prize`` directory be version controlled with
git.  We start with the original files for the paper:

.. prizerun::
    :hide:

    # Delete the current contents of 'nobel_prize'
    rm -rf .
    rm -rf .fancy_backups

.. runblock::

    unzip -o nobel_prize_files.zip
    cd nobel_prize

Create git repository:

.. prizerun::

    git init

What happened when we did ``git init``? Just what we were expecting; a
*repository* directory called ``.git``

.. prizerun::

    ls .git

The ``objects`` directory looks familiar. What's in there?

.. prizerun::

    tree .git/objects

Nothing but a couple of empty directories. That makes sense.

git add - put stuff into the staging area
=========================================

.. prizerun::

    git add nobel_prize_paper.txt

.. prizerun::

    tree .git/objects

Doing ``git add nobel_prize_paper.txt`` has added a file to the
``.git/objects`` directory. That filename looks suspiciously like a
hash.

We expect that ``git add`` added the file to the *staging area*. Have we
got any evidence of that?

.. prizerun::

    git status

Looking at real git objects
===========================

Git objects are nearly as simple as the objects we were writing in
``.fancy_backups``.

The main difference is that, to save space, they are compressed, in fact
using a library called ``zlib``.

These objects are so simple that it's very easy to write small code snippets
to read them - see :doc:`reading_git_objects`.

Git will also show the contents of objects with ``git show``.

When we did ``git add nobel_prize_paper.txt``, we got a new file in
``.git/objects``, with filename ``d9/2d079af6a7f276cc8d63dcf2549c03e7deb553``.
The filename is in fact a hash, where the first two digits form the directory
name (``d9``) and the rest of the filename is the rest of the hash digits
[#git-object-dir]_.

Here's the contents of the object:

.. prizerun::

    git show d92d079af6a7f276cc8d63dcf2549c03e7deb553

Just as we expected, it is the current contents of the
``nobel_prize_paper.txt``.

In fact we only need to give git enough hash digits for git to uniquely
identify the object.  7 digits if often enough, as in:

.. prizerun::

    git show d92d079

Staging the other files
=======================

.. prizerun::

    git add stunning_figure.png
    git add very_clever_analysis.py
    git status

We have now staged all three of our files.  We have three objects in
``.git/objects``:

.. prizerun::

    tree .git/objects

git commit - making the snapshot
================================

.. prizerun::

    git commit -m "First backup of my amazing idea"

In the line above, we used the ``-m`` flag to specify a message at the
command line. If we don't do that, git will open the editor we specified
in our configuration above and require that we enter a message. By
default, git refuses to record changes that don't have a message to go
along with them (though you can obviously 'cheat' by using an empty or
meaningless string: git only tries to facilitate best practices, it's
not your nanny).

We are now expecting to have two new ``.git/object`` files, for the directory
tree, and for the commit.

.. prizerun::

    tree .git/objects

Here's ``git show`` for the tree (directory listing):

.. prizerun::

    git show e129806

We can get a little more detail from the directory listing with ``git
ls-tree``:

.. prizerun::

    git ls-tree e129806

These are in fact the file permissions, the type of file (another directory,
or a file), the file hashes, and the file names.

git log - what are the commits so far?
======================================

.. prizerun::

    git log

I can also ask to the parents of each commit in the log:

.. prizerun::

    git log --parents

Why are these two outputs the same?

git branch - which branch are we on?
====================================

We haven't covered branches yet. Branches are bookmarks. They label the
commit we are on at the moment, and they track the commits as we do new
ones.

The default branch for git is called ``master``. Git creates it
automatically when you do your first commit.

.. prizerun::

    git branch

Asking for more verbose detail shows us that the branch is pointing to a
particular commit (where the commit is given by a hash):

.. prizerun::

    git branch -v

A branch is just a bookmark - a name that points to a commit.  In fact, git
stores branches as tiny text files, where the filename is the name of the
branch, and the contents is the hash of the commit that it points to:

.. prizerun::

    ls .git/refs/heads

.. prizerun::

    cat .git/refs/heads/master

git diff - what has changed?
============================

Let's do a little bit more work... Again, in practice you'll be editing
the files by hand, here we do it via shell commands for the sake of
automation (and therefore the reproducibility of this tutorial!)

.. prizerun::

    echo "The charts are very impressive" >> nobel_prize_paper.txt

And now we can ask git what is different:

.. prizerun::

    git diff

You need to ``git add`` a file to put it into the staging area
==============================================================

Remember that git only commits stuff that has been added to the staging
area.

At the moment we have changes that have not been staged:

.. prizerun::

    git status

If we try and do a commit, git will tell us there is nothing to commit,
because nothing has been staged:

.. prizerun::

    git commit

Git distinguishes three types of files
======================================

Files can be:

* unknown to git ("untracked")
* known to git but modified from the version in the last commit
* known to git and unmodified

The cycle of git virtue: work, commit, work, commit, ...
========================================================

We've done some work in the working tree, and we check what changes there are
that we might want to commit:

.. prizerun::

    git status

We add the changes for one edited file to the staging area:

.. prizerun::

    git add nobel_prize_paper.txt

We check that git is planning to add the changes to the paper to the next
commit:

.. prizerun::

    git status

We do the commit:

.. prizerun::

    git commit -m "Fruit of enormous thought"

Git updates the current branch with the latest commit
=====================================================

Remember branches?  Git has now moved the "master" branch bookmark up to the
new commit:

.. prizerun::

    git log

.. prizerun::

    git branch -v

.. prizerun::

    cat .git/refs/heads/master

The first commit is the parent of the first:

.. prizerun::

    git log --parents

A nicer log command using ``git config``
========================================

It is very often useful to see a summarized version of the log.  Here is a
useful version of the git log command:

.. prizerun::

    git log --oneline --topo-order --graph

Git supports *aliases:* new names given to command combinations. Let's
make this handy shortlog an alias, so we only have to type ``git slog``
to get this compact log:

.. prizerun::

    # We create our alias (this saves it in git's permanent configuration file):
    git config --global alias.slog "log --oneline --topo-order --graph"

    # And now we can use it
    git slog

``git mv`` and ``rm``: moving and removing files
================================================

While ``git add`` is used to add files to the list git tracks, we must
also tell it if we want their names to change or for it to stop tracking
them. In familiar Unix fashion, the ``mv`` and ``rm`` git commands do
precisely this:

.. prizerun::

    git mv very_clever_analysis.py slightly_dodgy_analysis.py
    git status

Note that these changes must be committed too, to become permanent! In
git's world, until something has been committed, it isn't permanently
recorded anywhere.

.. prizerun::

    git commit -m "I like this new name better"

.. prizerun::

    git slog

And ``git rm`` works in a similar fashion.

Exercise
========

Add a new file ``file2.txt``, commit it, make some changes to it, commit
them again, and then remove it (and don't forget to commit this last
step!).

Local user, branching
=====================

What is a branch? Simply a *label for the 'current' commit in a sequence
of ongoing commits*:

.. raw:: html

   <!-- offline: 

   ![](files/fig/masterbranch.png)

   -->

There can be multiple branches alive at any point in time; the working
directory is the state of a special pointer called HEAD. In this example
there are two branches, *master* and *testing*, and *testing* is the
currently active branch since it's what HEAD points to:

.. raw:: html

   <!-- offline: 

   ![](files/fig/HEAD_testing.png)

   -->

.. prizerun::

    cat .git/HEAD

.. prizerun::

    cat .git/refs/heads/master

.. prizerun::

    git branch -v

Once new commits are made on a branch, HEAD and the branch label move
with the new commits:

.. raw:: html

   <!-- offline: 

   ![](files/fig/branchcommit.png)

   -->

This allows the history of both branches to diverge:

.. raw:: html

   <!-- offline: 

   ![](files/fig/mergescenario.png)

   -->

But based on this graph structure, git can compute the necessary
information to merge the divergent branches back and continue with a
unified line of development:

.. raw:: html

   <!-- offline: 

   ![](files/fig/mergeaftermath.png)

   -->

Let's now illustrate all of this with a concrete example. Let's get our
bearings first:

.. prizerun::

    git status
    ls

We are now going to try two different routes of development: on the
``master`` branch we will add one file and on the ``experiment`` branch,
which we will create, we will add a different one. We will then merge
the experimental branch into ``master``.

.. prizerun::

    git branch experiment

What just happened? We made a branch, which is a pointer to this same
commit:

.. prizerun::

    ls .git/refs/heads

.. prizerun::

    git branch -v

.. prizerun::

    cat .git/refs/heads/experiment

How do we start working on this branch ``experiment`` rather than
``master``?

git checkout - set the current branch, set the working tree from a commit
=========================================================================

Up until now we have been on the ``master`` branch. When we make a
commit, the ``master`` branch pointer (``.git/refs/heads/master``) moves
up to track our most recent commit.

``git checkout`` can switch us to using another branch:

.. prizerun::

    git checkout experiment

What just happened?

.. prizerun::

    git branch -v

.. prizerun::

    cat .git/HEAD

As we'll see later, ``git checkout somebranch`` also sets the contents
of the working tree to match the commit contents for ``somebranch``. In
this case the commits for ``master`` and ``experiment`` are currently
the same, so we don't change the working tree at all.

Now let's do some changes on our ``experiment`` branch:

.. prizerun::

    echo "Some crazy idea" > experiment.txt
    git add experiment.txt
    git commit -m "Trying something new"
    git slog

Notice we have a new file called ``experiment.txt`` in this branch:

.. prizerun::

    ls

The ``experiment`` branch has now moved:

.. prizerun::

    cat .git/refs/heads/experiment

git checkout again - reseting the working tree
==============================================

If ``somewhere`` is a branch name, then ``git checkout somewhere``
selects ``somewhere`` as the current branch. It also resets the working
tree to match the working tree for that commit.

.. prizerun::

    git checkout master
    cat .git/HEAD

We're back to the working tree as of the ``master`` branch;
``experiment.txt`` has gone now.

.. prizerun::

    ls

Meanwhile we do some more work on master:

.. prizerun::

    git slog

.. prizerun::

    echo "All the while, more work goes on in master..." >> nobel_prize_paper.txt
    git add nobel_prize_paper.txt
    git commit -m "The mainline keeps moving"
    git slog

.. prizerun::

    ls

Now let's do the merge

.. prizerun::

    git merge experiment -m "Merge in the experiment"

.. prizerun::

    git slog

An important aside: conflict management
=======================================

While git is very good at merging, if two different branches modify the
same file in the same location, it simply can't decide which change
should prevail. At that point, human intervention is necessary to make
the decision. Git will help you by marking the location in the file that
has a problem, but it's up to you to resolve the conflict. Let's see how
that works by intentionally creating a conflict.

We start by creating a branch and making a change to our experiment
file:

.. prizerun::

    git branch trouble
    git checkout trouble
    echo "This is going to be a problem..." >> experiment.txt
    git add experiment.txt
    git commit -m"Changes in the trouble branch"

And now we go back to the master branch, where we change the *same*
file:

.. prizerun::

    git checkout master
    echo "More work on the master branch..." >> experiment.txt
    git add experiment.txt
    git commit -m"Mainline work"

More configuration for fuller output
====================================

This line tells git how to show conflicts in text files.

See ``git config --help`` and look for ``merge.conflictstyle`` for more
information.

This setting asks git to show:

-  The original file contents from ``HEAD``, the commit tree that you
   are merging *into*
-  The contents of the file as of last common ancestor commit
-  The new file contents from the commit tree that you are merging
   *from*

.. prizerun::

    git config merge.conflictstyle diff3

So now let's see what happens if we try to merge the ``trouble`` branch
into ``master``:

.. prizerun::

    git merge trouble -m "Unlikely this one will work"

Let's see what git has put into our file:

.. prizerun::

    cat experiment.txt

Read this as:

-  Common ancestor (between ``||``... and ``==``) has nothing;
-  ``HEAD`` - the current branch - (between ``<<``... and ``||``) adds
   ``More work on the master branch...``;
-  the ``trouble`` branch (between ``==``... and ``>>``...) adds
   ``This is going to be a problem...``.

At this point, we go into the file with a text editor, decide which
changes to keep, and make a new commit that records our decision.

I'll do the edits by writing the file I want directly in this case:

.. prizewrite::

    # file: experiment.txt
    Some crazy idea
    More work on the master branch...
    This is going to be a problem...

I've now made the edits. I decided that both pieces of text were useful,
but integrated them with some changes:

.. prizerun::

    git status

Let's then make our new commit:

.. prizerun::

    git add experiment.txt
    git commit -m "Completed merge of trouble, fixing conflicts along the way"
    git slog

Other useful commands
=====================

-  `show <http://www.kernel.org/pub/software/scm/git/docs/git-show.html>`__

-  `reflog <http://www.kernel.org/pub/software/scm/git/docs/git-reflog.html>`__

-  `rebase <http://www.kernel.org/pub/software/scm/git/docs/git-rebase.html>`__

-  `tag <http://www.kernel.org/pub/software/scm/git/docs/git-tag.html>`__

Git resources
=============

Introductory materials
======================

There are lots of good tutorials and introductions for Git, which you
can easily find yourself; this is just a short list of things I've found
useful. For a beginner, I would recommend the following 'core' reading
list, and below I mention a few extra resources:

1. The smallest, and in the style of this tuorial: `git - the simple
   guide <http://rogerdudler.github.com/git-guide>`__ contains 'just the
   basics'. Very quick read.

2. The concise `Git Reference <http://gitref.org>`__: compact but with
   all the key ideas. If you only read one document, make it this one.

3. In my own experience, the most useful resource was `Understanding Git
   Conceptually <http://www.sbf5.com/~cduan/technical/git>`__. Git has a
   reputation for being hard to use, but I have found that with a clear
   view of what is actually a *very simple* internal design, its
   behavior is remarkably consistent, simple and comprehensible.

4. For more detail, see the start of the excellent `Pro
   Git <http://progit.org/book>`__ online book, or similarly the early
   parts of the `Git community book <http://book.git-scm.com>`__. Pro
   Git's chapters are very short and well illustrated; the community
   book tends to have more detail and has nice screencasts at the end of
   some sections.

If you are really impatient and just want a quick start, this `visual
git
tutorial <http://www.ralfebert.de/blog/tools/visual_git_tutorial_1>`__
may be sufficient. It is nicely illustrated with diagrams that show what
happens on the filesystem.

For windows users, `an Illustrated Guide to Git on
Windows <http://nathanj.github.com/gitguide/tour.html>`__ is useful in
that it contains also some information about handling SSH (necessary to
interface with git hosted on remote servers when collaborating) as well
as screenshots of the Windows interface.

Cheat sheets
    Two different
    `cheat <http://zrusin.blogspot.com/2007/09/git-cheat-sheet.html>`__
    `sheets <http://jan-krueger.net/development/git-cheat-sheet-extended-edition>`__
    in PDF format that can be printed for frequent reference.

Beyond the basics
=================

As you've seen, this tutorial makes the bold assumption that you'll be
able to understand how git works by seeing how it is *built*. These two
documents, written in a similar spirit, are probably the most useful
descriptions of the Git architecture short of diving into the actual
implementation. They walk you through how you would go about building a
version control system with a little story. By the end you realize that
Git's model is almost an inevitable outcome of the proposed constraints:

-  The `Git
   parable <http://tom.preston-werner.com/2009/05/19/the-git-parable.html>`__
   by Tom Preston-Werner.
-  `Git
   foundations <http://matthew-brett.github.com/pydagogue/foundation.html>`__
   by Matthew Brett.

`Git ready <http://www.gitready.com>`__
    A great website of posts on specific git-related topics, organized
    by difficulty.

`QGit <http://sourceforge.net/projects/qgit/>`__: an excellent Git GUI
    Git ships by default with gitk and git-gui, a pair of Tk graphical
    clients to browse a repo and to operate in it. I personally have
    found `qgit <http://sourceforge.net/projects/qgit/>`__ to be nicer
    and easier to use. It is available on modern linux distros, and
    since it is based on Qt, it should run on OSX and Windows.

`Git Magic <http://www-cs-students.stanford.edu/~blynn/gitmagic/index.html>`_ :
    Another book-size guide that has useful snippets.

The `learning center <http://learn.github.com>`__ at Github
    Guides on a number of topics, some specific to github hosting but
    much of it of general value.

A `port <http://cworth.org/hgbook-git/tour>`__ of the Hg book's beginning
    The `Mercurial book <http://hgbook.red-bean.com>`__ has a reputation
    for clarity, so Carl Worth decided to
    `port <http://cworth.org/hgbook-git/tour>`__ its introductory
    chapter to Git. It's a nicely written intro, which is possible in
    good measure because of how similar the underlying models of Hg and
    Git ultimately are.

`Intermediate tips <http://andyjeffries.co.uk/articles/25-tips-for-intermediate-git-users>`_: A set
    of tips that contains some very valuable nuggets, once you're past the basics.

For SVN users
=============

If you want a bit more background on why the model of version control
used by Git and Mercurial (known as distributed version control) is such
a good idea, I encourage you to read this very well written
`post <http://www.joelonsoftware.com/items/2010/03/17.html>`__ by Joel
Spolsky on the topic. After that post, Joel created a very nice
Mercurial tutorial, whose `first page <http://hginit.com/00.html>`__
applies equally well to git and is a very good 're-education' for anyone
coming from an SVN (or similar) background.

In practice, I think you are better off following Joel's advice and
understanding git on its own merits instead of trying to bang SVN
concepts into git shapes. But for the occasional translation from SVN to
Git of a specific idiom, the `Git - SVN Crash
Course <http://git-scm.org/course/svn.html>`__ can be handy.

A few useful tips for common tasks
==================================

Better shell support
--------------------

Adding git branch info to your bash prompt and tab completion for git
commands and branches is extremely useful. I suggest you at least copy:

-  `git-completion.bash <https://github.com/git/git/blob/master/contrib/completion/git-completion.bash>`__

-  `git-prompt.sh <https://github.com/git/git/blob/master/contrib/completion/git-prompt.sh>`__

You can then source both of these files in your ``~/.bashrc`` (Linux) or
``~/.bash_profile`` (OSX), and then set your prompt (I'll assume you
named them as the originals but starting with a ``.`` at the front of
the name):

::

    source $HOME/.git-completion.bash

    source $HOME/.git-prompt.sh

    PS1='[\u@\h \W$(__git_ps1 " (%s)")]\$ '   # adjust this to your prompt liking

See the comments in both of those files for lots of extra functionality
they offer.

Embedding Git information in LaTeX documents
--------------------------------------------

(Sent by `Yaroslav Halchenko <http://www.onerussian.com>`__)

I use a Make rule:

::

    # Helper if interested in providing proper version tag within the manuscript
    revision.tex: ../misc/revision.tex.in ../.git/index
       GITID=$$(git log -1 | grep -e '^commit' -e '^Date:' | sed  -e 's/^[^ ]* *//g' | tr '\n' ' '); \
       echo $$GITID; \
       sed -e "s/GITID/$$GITID/g" $< >| $@

in the top level ``Makefile.common`` which is included in all
subdirectories which actually contain papers (hence all those
``../.git``). The ``revision.tex.in`` file is simply:

::

    % Embed GIT ID revision and date
    \def\revision{GITID}

The corresponding ``paper.pdf`` depends on ``revision.tex`` and includes
the line ``\input{revision}`` to load up the actual revision mark.

git export
----------

Git doesn't have a native export command, but this works just fine:

::

    git archive --prefix=fperez.org/  master | gzip > ~/tmp/source.tgz

.. rubric:: Footnotes

.. [#git-object-dir] When git stores a file in the ``.git/objects`` directory,
   it does a hash for the file, takes the first two digits of the hash to make
   a directory, and then stores a file with a filename from the remaining hash
   digits.  For example, when adding a file with hash
   ``d92d079af6a7f276cc8d63dcf2549c03e7deb553`` git will create
   ``.git/objects/d9`` directory if it doesn't exist, and stores the file
   contents as ``.git/objects/d9/2d079af6a7f276cc8d63dcf2549c03e7deb553``.  It
   does this so that the number of files in any one directory stay in a
   reasonable range.  If git had to store every file, directory listing and
   commit in one flat directory, it would soon have a very large number of
   files.

.. include:: links_names.inc
