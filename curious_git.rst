.. check with make doctest

####################################
The curious coder's guide to ``git``
####################################

*****************
git - love - hate
*****************

I've used git now for a long time.  I think it's a true masterpiece of design, I
use it all day every day and I just can't imagine what it would be like not to
use it. So, no question, I *love* git.

As y'all may know, `Linus Torvalds wrote git from scratch
<http://git-scm.com/book/en/Getting-Started-A-Short-History-of-Git>`_.  He loves
it too.  `Here is Linus talking about git
<http://www.youtube.com/watch?v=MShbP3OpASA#t=2288>`_ in a question and answer
session:

    Actually I'm proud of git. I want to say this. The fact that I had to write
    git was accidental, but Linux, the design came from a great mind, and that
    great mind was not mine. I mean you have to give credit for the design of
    Linux to Kernighan and Ritchie and Thompson. I mean there's a reason I like
    Unix and I wanted to redo it. I do want to say that git is a design that is
    mine and unique, and I'm proud of the fact that I can damn well also do good
    design from scratch.

But - some people hate git.  Really *hate* it. They find it confusing and error
prone and it makes them angry.  Why are there such different views?

I think the reason some people hate git, is because they don't yet understand
it.  I reason I can say this without being patronizing is because I went through
something similar myself.

When I first started using git, I found it uncomfortable.  I could see it was
very powerful, but I sometimes got lost and stuck and had to Google for a set of
magic commands to get me out of trouble.  I once accidentally made a huge mess
of our project's main repository by running a command I didn't understand. Git
often made me feel stupid.  It felt like a prototype racecar with a badly
designed dashboard that was just about to blow an engine or a tire and take me
off the road.

Then, one day, I read the `git parable`_.  The git parable is a little story
about a developer trying to work out how to make a version control system.  It
gradually builds up from copying whole directories of files to something very
much like git.  I didn't understand it all right away, but as soon as I read this
page, the light-bulb went on - I got git.  I suddenly started to feel
comfortable.  I knew for sure I could work out why git worked the way it did.  I
could see that it must be possible how to do complicated and powerful things,
and I could work out how to do them.

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
    that it can be confusing and unnecessarily complex for beginners. Thus, I’ve
    made this discussion the last chapter in the book so you could read it early
    or later in your learning process. I leave it up to you to decide.

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

*******************
The story so far...
*******************

You are writing a breakthrough paper showing that you can entirely
explain the brain using random numbers. You've got the draft paper, and
the analysis script and a figure for the paper. These are all in a
directory modestly named ``nobel_prize``.

In this directory, you have the paper draft ``nobel_prize.txt``, the
analysis script ``very_clever_analysis.py``, and a figure for the paper
``stunning_figure.png``.

You can get this ground-breaking paper by downloading and unzipping
:download:`nobel_prize_files.zip`.

.. cleanup

.. runblock::
    :hide:

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

.. runblock:: bash
    :cwd: nobel_prize

    mkdir .fancy_backups

Then you make a directory for the first backup:

.. runblock:: bash
    :cwd: nobel_prize

    mkdir .fancy_backups/1
    mkdir .fancy_backups/1/files

And you copy the files there:

.. runblock:: bash
    :cwd: nobel_prize

    cp * .fancy_backups/1/files

Reminding yourself of what you did
==================================

For good measure, you put a file in the snapshot directory to remind you when
you did the snapshot, and who did it, and what was new for this snapshot

.. code:: python

    %%file .fancy_backups/1/info.txt
    Date: April 1 2012, 14.30
    Author: I. M. Awesome
    Notes: First backup of my amazing idea

.. parsed-literal::

    Writing .fancy_backups/1/info.txt


Now you have these files in the ``nobel_prize`` directory:

.. runblock:: bash
    :cwd: nobel_prize

    tree

Every time you do some work on the files, you back them up in the same
way. After a few days:

.. code:: python

    !echo "The charts are very impressive\n" >> nobel_prize.txt
    !mkdir .fancy_backups/2
    !mkdir .fancy_backups/2/files
    !cp * .fancy_backups/2/files
.. code:: python

    %%file .fancy_backups/2/info.txt
    Date: April 1 2012, 18.03
    Author: I. M. Awesome
    Notes: Fruit of enormous thought

.. parsed-literal::

    Writing .fancy_backups/2/info.txt


.. code:: python

    !echo "The graphs are also compelling\n" >> nobel_prize.txt
    !mkdir .fancy_backups/3
    !mkdir .fancy_backups/3/files
    !cp * .fancy_backups/3/files

.. code:: python

    %%file .fancy_backups/3/info.txt
    Date: April 2 2012, 11.20
    Author: I. M. Awesome
    Notes: Now seeing things clearly

.. code:: python

    print_tree()

.. parsed-literal::

    ├── [94m.fancy_backups[0m
    │   ├── [94m1[0m
    │   │   ├── [94mfiles[0m
    │   │   │   ├── nobel_prize.txt
    │   │   │   ├── stunning_figure.png
    │   │   │   └── very_clever_analysis.py
    │   │   └── info.txt
    │   ├── [94m2[0m
    │   │   ├── [94mfiles[0m
    │   │   │   ├── nobel_prize.txt
    │   │   │   ├── stunning_figure.png
    │   │   │   └── very_clever_analysis.py
    │   │   └── info.txt
    │   └── [94m3[0m
    │       ├── [94mfiles[0m
    │       │   ├── nobel_prize.txt
    │       │   ├── stunning_figure.png
    │       │   └── very_clever_analysis.py
    │       └── info.txt
    ├── nobel_prize.txt
    ├── stunning_figure.png
    └── very_clever_analysis.py


.. code:: python

    # Now we just cheat, and copy the commits
    !cp -r .fancy_backups/3 .fancy_backups/4
    !cp -r .fancy_backups/3 .fancy_backups/5
    !cp -r .fancy_backups/3 .fancy_backups/6

You keep doing this, until again the day comes to talk to Josephine. You
now have 5 backups.

The future has not changed. Josephine again thinks the results have
changed. But now - you can check.

You go back and look at ``.fancy_backups/1/stunning_figure.png``. It
does look different.

You go through all the ``.fancy_backups`` directories in order. It turns
out that the figure changes in ``.fancy_backups/4``.

You look in ``.fancy_backups/4/info.txt`` and it says:

::

    Date: April 8 2012, 01.40
    Author: I. M. Awesome
    Notes: I always get the best ideas after I have been drinking.


Aha. Then you go find the problem in
``fancy_backups/4/very_clever_analysis.py``.

You fix ``very_clever_analysis.py``.

You make a new snapshot ``.fancy_backups/6``.

Back on track for a scientific breakthrough

Terminology breakout
====================

Here are some
`terms <https://www.kernel.org/pub/software/scm/git/docs/gitglossary.html>`__.

-  Working tree: the files you are working on in the current directory
   (``nobel_prize``). The files ``very_clever_analysis.py``,
   ``nobel_prize.txt``, ``stunning_figure.png`` are the files in your
   working tree
-  Repository: the directory containing information about the history of
   the files. Your directory ``.fancy_snapshot`` is the repository.
-  Commit: a completed snapshot. For example, ``.fancy_backups/1``
   contains one commit.

We'll use these terms to get used to them.

Breaking up work into chunks
============================

You did some edits to the paper ``nobel_prize.txt`` to edit the
introduction.

You also had a good idea for the analysis, and did some edits to
``very_clever_analysis.py``.

You've got used to breaking each new *commit* (snapshot) up into little
bits of extra work, with their own comments in the ``info.txt``.

You want to make two commits from your changes:

1. a commit containing the changes to ``nobel_prize.txt``, with comment
   "Changes to introduction"
2. a commit containing the changes to ``very_clever_analysis.py`` with
   comment "Crazy new analysis"

How can I do that?

The staging area
================

We adapt the workflow. Each time we start work, after a commit, we copy
the last commit to directory ``.fancy_backups/staging_area``. That will
the default contents of our next commit.

.. code:: python

    !mkdir .fancy_backups/staging_area
    !cp .fancy_backups/6/files/* .fancy_backups/staging_area
    !ls .fancy_backups/staging_area

.. parsed-literal::

    nobel_prize.txt         stunning_figure.png     very_clever_analysis.py


Now, you do your edits to ``nobel_prize.txt``, and
``very_clever_analysis.py`` in your *working tree* (the ``nobel_prize``
directory). Then you get ready for the next commit with:

.. code:: python

    !cp nobel_prize.txt .fancy_backups/staging_area

The staging area now contains all the files for the upcoming commit
(snapshot).

You make the commit with:

.. code:: python

    !mkdir .fancy_backups/7
    !mkdir .fancy_backups/7/files
    !cp .fancy_backups/staging_area/* .fancy_backups/7/files

.. code:: python

    %%file .fancy_backups/7/info.txt
    Date: April 10 2012, 14.30
    Author: I. M. Awesome
    Notes: Changes to introduction

.. parsed-literal::

    Writing .fancy_backups/7/info.txt


Now you are ready for the next commit, with the changes to the analysis
script.

.. code:: python

    !cp very_clever_analysis.py .fancy_backups/staging_area

The commit is now *staged* and ready to be saved.

.. code:: python

    # Our commit procedure; same as last time with "8" instead of "7"
    !mkdir .fancy_backups/8
    !mkdir .fancy_backups/8/files
    !cp .fancy_backups/staging_area/* .fancy_backups/8/files

.. code:: python

    %%file .fancy_backups/8/info.txt
    Date: April 10 2012, 14.35
    Author: I. M. Awesome
    Notes: Crazy new analysis

.. parsed-literal::

    Writing .fancy_backups/8/info.txt


Here is what we have in our ``.fancy_backups`` directory:

.. code:: python

    print_tree('.fancy_backups')

.. parsed-literal::

    ├── [94m1[0m
    │   ├── [94mfiles[0m
    │   │   ├── nobel_prize.txt
    │   │   ├── stunning_figure.png
    │   │   └── very_clever_analysis.py
    │   └── info.txt
    ├── [94m2[0m
    │   ├── [94mfiles[0m
    │   │   ├── nobel_prize.txt
    │   │   ├── stunning_figure.png
    │   │   └── very_clever_analysis.py
    │   └── info.txt
    ├── [94m3[0m
    │   ├── [94mfiles[0m
    │   │   ├── nobel_prize.txt
    │   │   ├── stunning_figure.png
    │   │   └── very_clever_analysis.py
    │   └── info.txt
    ├── [94m4[0m
    │   ├── [94mfiles[0m
    │   │   ├── nobel_prize.txt
    │   │   ├── stunning_figure.png
    │   │   └── very_clever_analysis.py
    │   └── info.txt
    ├── [94m5[0m
    │   ├── [94mfiles[0m
    │   │   ├── nobel_prize.txt
    │   │   ├── stunning_figure.png
    │   │   └── very_clever_analysis.py
    │   └── info.txt
    ├── [94m6[0m
    │   ├── [94mfiles[0m
    │   │   ├── nobel_prize.txt
    │   │   ├── stunning_figure.png
    │   │   └── very_clever_analysis.py
    │   └── info.txt
    ├── [94m7[0m
    │   ├── [94mfiles[0m
    │   │   ├── nobel_prize.txt
    │   │   ├── stunning_figure.png
    │   │   └── very_clever_analysis.py
    │   └── info.txt
    ├── [94m8[0m
    │   ├── [94mfiles[0m
    │   │   ├── nobel_prize.txt
    │   │   ├── stunning_figure.png
    │   │   └── very_clever_analysis.py
    │   └── info.txt
    └── [94mstaging_area[0m
        ├── nobel_prize.txt
        ├── stunning_figure.png
        └── very_clever_analysis.py


Now the very difficult problem
==============================

Let's say that the figure ``stunning_figure.png`` is large.

Let's say it changes only once across our 8 commits, at commit 5.

What should we do to save disk space for ``.fancy_backups``?

********************
Cryptographic hashes
********************

Later on, I'm going to ask you to solve a very difficult problem.

Here's some background that might help.

I'm going to describe "Crytographic hashes". It won't be obvious why
that's a good idea for a little while.

See : `Wikipedia on hash
functions <http://en.wikipedia.org/wiki/Cryptographic_hash_function>`__.

A *hash* is the result of running a *hash function* over a block of
data. The hash is a fixed length string that is the *signature* of that
exact block of data. Let's run this in Python:

.. doctest::

    >>> import hashlib
    >>> sha1_hash_function = hashlib.sha1
    >>> message = "git is a rude word in UK English"
    >>> hash_value = sha1_hash_function(message).hexdigest()
    >>> hash_value
    'fec41478c4f497c1d90fd28610f4272c78a6867e'

Not too exciting so far. However, the rather magical nature of this
string is not yet apparent. Here's the trick:

**There is no practical way for you to find another ``message`` that
will give the same ``hash_value``**

The ``hash_value`` then is (nearly) completely unique to that set of
bytes.

For example, a tiny change in the string makes the hash completely
different. Here I've just added a full stop at the end:

.. doctest::
    >>> sha1_hash_function("git is a rude word in UK English.").hexdigest()
    '9e87add001f13aa79ed7b42a5effbfc60aa8584e'

So, if you give me some data, and I calculate the hash value, and it
comes out as "fec41478c4f497c1d90fd28610f4272c78a6867e", then I can be
very sure that the data you gave me was exactly the string "git is a
rude word in UK English".

Exercise - your strategy
========================

Split into pairs.

In five minutes, we'll share ideas.

My crazy idea - use hash values as file names
=============================================

Make a new directory:

.. code:: python

    !mkdir .fancy_backups/objects

Calculate the hash value for the figure:

.. code:: python

    import hashlib
    # read the bytes for the figure into a string
    figure_data = open('.fancy_backups/1/files/stunning_figure.png', 'rb').read()
    # Calculate the hash value
    figure_hash = hashlib.sha1(figure_data).hexdigest()
    figure_hash


.. parsed-literal::

    'aff88ecead2c7166770969a54dc855c8b91be864'



Save the figure with the hash value as the file name:

.. code:: python

    !cp .fancy_backups/1/files/stunning_figure.png .fancy_backups/objects/$figure_hash

Do the same for the other two files in the first commit.

.. code:: python

    import os
    
    def copy_to_hash(fname):
        # Read the data
        binary_data = open(fname, 'rb').read()
        # Find the hash
        hash_value = hashlib.sha1(binary_data).hexdigest()
        # Save with the hash filename
        hash_fname = '.fancy_backups/objects/' + hash_value
        if os.path.isfile(hash_fname):
            print "We already have a hash file for " + fname
        else:
            open(hash_fname, 'wb').write(binary_data)
        return hash_value

.. code:: python

    paper_hash = copy_to_hash('.fancy_backups/1/files/nobel_prize.txt')
    script_hash = copy_to_hash('.fancy_backups/1/files/very_clever_analysis.py')

Making the directory listing
============================

Here are the hashes for all files:

.. code:: python

    print 'Hash for stunning_figure.png:', figure_hash
    print 'Hash for nobel_prize:', paper_hash
    print 'Hash for very_clever_analysis.py:', script_hash

.. parsed-literal::

    Hash for stunning_figure.png: aff88ecead2c7166770969a54dc855c8b91be864
    Hash for nobel_prize: 3af8809ecb9c6dec33fc7e5ad330e384663f5a0d
    Hash for very_clever_analysis.py: e7f3ca9157fd7088b6a927a618e18d4bc4712fb6


.. code:: python

    print_tree('.fancy_backups/objects')

.. parsed-literal::

    ├── 3af8809ecb9c6dec33fc7e5ad330e384663f5a0d
    ├── aff88ecead2c7166770969a54dc855c8b91be864
    └── e7f3ca9157fd7088b6a927a618e18d4bc4712fb6


Now point the snapshot to the hash filename versions of the files by
making a *text directory listing* or *tree* listing:

.. code:: python

    %%file .fancy_backups/1/directory_list
    Filename                Hash value
    ========                ==========
    stunning_figure.png     aff88ecead2c7166770969a54dc855c8b91be864
    nobel_prize.txt         3af8809ecb9c6dec33fc7e5ad330e384663f5a0d
    very_clever_analysis.py e7f3ca9157fd7088b6a927a618e18d4bc4712fb6

.. parsed-literal::

    Writing .fancy_backups/1/directory_list


The next commit - saves space!
==============================

.. code:: python

    # Nothing to for unchanged figure - already have hash value file
    figure_hash = copy_to_hash('.fancy_backups/2/files/stunning_figure.png')
    # Makes a new copy
    paper_hash = copy_to_hash('.fancy_backups/2/files/nobel_prize.txt')
    # Nothing to for unchanged script - already have hash value file
    script_hash = copy_to_hash('.fancy_backups/2/files/very_clever_analysis.py')
    print 'Hash for stunning_figure.png:', figure_hash
    print 'Hash for nobel_prize:', paper_hash
    print 'Hash for very_clever_analysis.py:', script_hash

.. parsed-literal::

    We already have a hash file for .fancy_backups/2/files/stunning_figure.png
    We already have a hash file for .fancy_backups/2/files/very_clever_analysis.py
    Hash for stunning_figure.png: aff88ecead2c7166770969a54dc855c8b91be864
    Hash for nobel_prize: bc330d8886bb1b36a49d8e7ebb07d3443190b0e6
    Hash for very_clever_analysis.py: e7f3ca9157fd7088b6a927a618e18d4bc4712fb6


Only the ``nobel_prize.txt`` has changed. So:

.. code:: python

    %%file .fancy_backups/2/directory_list
    Filename                Hash value
    ========                ==========
    stunning_figure.png     aff88ecead2c7166770969a54dc855c8b91be864
    nobel_prize.txt         bc330d8886bb1b36a49d8e7ebb07d3443190b0e6
    very_clever_analysis.py e7f3ca9157fd7088b6a927a618e18d4bc4712fb6

.. parsed-literal::

    Writing .fancy_backups/2/directory_list


An even more crazy idea - hash the tree
=======================================

I guess we can store the tree for the first commit according to its
hash:

.. code:: python

    tree_hash = copy_to_hash('.fancy_backups/1/directory_list')
    tree_hash



.. parsed-literal::

    '63d466086dd359c0b34d21e04b812781c7153b23'



And we can do the same for the second commit:

.. code:: python

    copy_to_hash('.fancy_backups/2/directory_list')



.. parsed-literal::

    'd45095659d1ea567b90aaf923e265bf41cbb126f'

Now - would I get the same hash if I had had a different figure?

Even more crazy idea - make the whole commit into a text file
=============================================================

How about this?

.. code:: python

    %%file .fancy_backups/1/commit
    Date: April 1 2012, 14.30
    Author: I. M. Awesome
    Notes: First backup of my amazing idea
    Tree: 63d466086dd359c0b34d21e04b812781c7153b23

.. parsed-literal::

    Writing .fancy_backups/1/commit


And now I can hash the commit!

.. code:: python

    commit_hash = copy_to_hash('.fancy_backups/1/commit')
    commit_hash



.. parsed-literal::

    'f473e51a38d40772722205c92dddd4bdfd941ef8'



Would the commit hash value change if the figure changed?

So crazy it's actually git
==========================

Now look in ``.fancy_backups/objects``:

.. code:: python

    ls .fancy_backups/objects

.. parsed-literal::

    3af8809ecb9c6dec33fc7e5ad330e384663f5a0d  bc330d8886bb1b36a49d8e7ebb07d3443190b0e6  f473e51a38d40772722205c92dddd4bdfd941ef8
    63d466086dd359c0b34d21e04b812781c7153b23  d45095659d1ea567b90aaf923e265bf41cbb126f
    aff88ecead2c7166770969a54dc855c8b91be864  e7f3ca9157fd7088b6a927a618e18d4bc4712fb6


That's 3 file copies for the files from the first commit, 1 file copy
from the second commit, 2 directory listings (for first and second
commit) and one commit listing (for the first commit) = 7 hash objects.

We know that the file beginning 'f473e51' *completely defines the first
commit*:

.. code:: python

    !cat .fancy_backups/objects/f473e51a38d40772722205c92dddd4bdfd941ef8

.. parsed-literal::

    Date: April 1 2012, 14.30
    Author: I. M. Awesome
    Notes: First backup of my amazing idea
    Tree: 63d466086dd359c0b34d21e04b812781c7153b23

Linking the commits
===================

Can we completely get rid of ``.fancy_backups/1``, ``.fancy_backups/2``
-----------------------------------------------------------------------

The reason for our commit names "1","2", "3" was so we know that commit
"2" comes after commit "1" and before commit "3". Now our commits have
arbitrary hashes, we can't tell the order from the name.

We can specify the order by adding the commit hash of the previous
commit into the current commit:

.. code:: python

    %%file .fancy_backups/temporary_file
    Date: April 1 2012, 18.03
    Author: I. M. Awesome
    Notes: Fruit of enormous thought
    Tree: d45095659d1ea567b90aaf923e265bf41cbb126f
    Parent: 63dab6e48ed2e9111624a3b5391bdf784c040b86

.. parsed-literal::

    Writing .fancy_backups/temporary_file


.. code:: python

    commit2_hash = copy_to_hash('.fancy_backups/temporary_file')

Now we have the order of the commits from the links between them.

And now you are already a git master.

Gitting going (sorry)
^^^^^^^^^^^^^^^^^^^^^

**Note**: Much of the rest of this presentation comes from Fernando
Perez' excellent git tutorial in his `reproducible software
repository <https://github.com/fperez/reprosw>`__. Thanks to Fernando
for sharing.

We need to tell git about us before we start. This stuff will go into
the commit information.

.. code:: python

    !git config --global user.name "Matthew Brett"
    !git config --global user.email "matthew.brett@gmail.com"

git often needs to call up a text editor. Choose the editor you like
here:

.. code:: python

    # Put here your preferred editor. 
    !git config --global core.editor gedit

We also turn on the use of color, which is very helpful in making the
output of git easier to read

.. code:: python

    !git config --global color.ui "auto"

Getting help
============

.. code:: python

    !git

.. parsed-literal::

    usage: git [--version] [--exec-path[=<path>]] [--html-path] [--man-path] [--info-path]
               [-p|--paginate|--no-pager] [--no-replace-objects] [--bare]
               [--git-dir=<path>] [--work-tree=<path>] [--namespace=<name>]
               [-c name=value] [--help]
               <command> [<args>]
    
    The most commonly used git commands are:
       add        Add file contents to the index
       bisect     Find by binary search the change that introduced a bug
       branch     List, create, or delete branches
       checkout   Checkout a branch or paths to the working tree
       clone      Clone a repository into a new directory
       commit     Record changes to the repository
       diff       Show changes between commits, commit and working tree, etc
       fetch      Download objects and refs from another repository
       grep       Print lines matching a pattern
       init       Create an empty git repository or reinitialize an existing one
       log        Show commit logs
       merge      Join two or more development histories together
       mv         Move or rename a file, a directory, or a symlink
       pull       Fetch from and merge with another repository or a local branch
       push       Update remote refs along with associated objects
       rebase     Forward-port local commits to the updated upstream head
       reset      Reset current HEAD to the specified state
       rm         Remove files from the working tree and from the index
       show       Show various types of objects
       status     Show the working tree status
       tag        Create, list, delete or verify a tag object signed with GPG
    
    See 'git help <command>' for more information on a specific command.


Try ``git help add`` for an example.

Initializing the repository
===========================

Let's make this ``nobel_prize`` directory be version controlled with
git.

.. code:: python

    # First pull the contents of the first commit from .fancy_backups
    !cp .fancy_backups/1/files/* .
    # Then delete .fancy_backups - we're done with those guys
    !rm -rf .fancy_backups

.. code:: python

    !ls -a

.. parsed-literal::

    [34m.[m[m                       [34m..[m[m                      nobel_prize.txt         stunning_figure.png     very_clever_analysis.py


.. code:: python

    !git init

.. parsed-literal::

    Initialized empty Git repository in /Users/mb312/dev_trees/pna-notebooks/nobel_prize/.git/

Just what we were expecting; a *repository* directory called ``.git``

.. code:: python

    !ls .git

.. parsed-literal::

    HEAD        [34mbranches[m[m    config      [31mdescription[m[m [34mhooks[m[m       [34minfo[m[m        [34mobjects[m[m     [34mrefs[m[m


The ``objects`` directory looks familiar. What's in there?

.. code:: python

    print_tree('.git/objects')

.. parsed-literal::

    ├── [94minfo[0m
    └── [94mpack[0m


Nothing. That makes sense.

git add - put stuff into the staging area
=========================================

.. code:: python

    !git add nobel_prize.txt

.. code:: python

    print_tree('.git/objects')

.. parsed-literal::

    ├── [94md9[0m
    │   └── 2d079af6a7f276cc8d63dcf2549c03e7deb553
    ├── [94minfo[0m
    └── [94mpack[0m


Doing ``git add nobel_prize.txt`` has added a file to the
``.git/objects`` directory. That filename looks suspiciously like a
hash.

git add and the staging area
============================

We expect that ``git add`` added the file to the *staging area*. Have we
got any evidence of that?

.. code:: python

    !git status

.. parsed-literal::

    # On branch master
    #
    # Initial commit
    #
    # Changes to be committed:
    #   (use "git rm --cached <file>..." to unstage)
    #
    #	[32mnew file:   nobel_prize.txt[m
    #
    # Untracked files:
    #   (use "git add <file>..." to include in what will be committed)
    #
    #	[31mstunning_figure.png[m
    #	[31mvery_clever_analysis.py[m


Reading real git objects
========================

Git objects are nearly as simple as the objects we were writing in
``.fancy_backups``.

The main difference is that, to save space, they are compressed, in fact
using a library called ``zlib``.

Here's a routine that gives us the raw contents of stuff in the
``.git/objects`` directory. There are neater commands in git to do this,
but this shows just how simple these objects are.

.. code:: python

    import zlib # A compression / decompression library
    
    def read_git_object(filename):
        """ Read an object in the ``.git/objects`` directory
    
        Yes, it's this simple - in this case.  But git reserves the right to use
        more complicated storage formats to save space when your repository is larger
        """
        compressed_contents = open(filename, 'rb').read()
        return zlib.decompress(compressed_contents)

.. code:: python

    filename = '.git/objects/d9/2d079af6a7f276cc8d63dcf2549c03e7deb553'
    new_object_data = read_git_object(filename)
    print new_object_data

.. parsed-literal::

    blob 189 The brain is just a set of random numbers
    =========================================
    
    We have discovered that the brain is a set of random numbers.
    
    We have charts and graphs to back us up.
    


It's just the contents of the file, with some cruft at the start
(``blob 189``).

Staging the other files
=======================

.. code:: python

    !git add stunning_figure.png
    !git add very_clever_analysis.py

.. code:: python

    !git status

.. parsed-literal::

    # On branch master
    #
    # Initial commit
    #
    # Changes to be committed:
    #   (use "git rm --cached <file>..." to unstage)
    #
    #	[32mnew file:   nobel_prize.txt[m
    #	[32mnew file:   stunning_figure.png[m
    #	[32mnew file:   very_clever_analysis.py[m
    #


.. code:: python

    print_tree('.git/objects')

.. parsed-literal::

    ├── [94m8a[0m
    │   └── dc8bf371d669242ea998f78f9916867cc6203c
    ├── [94m9f[0m
    │   └── fc311b29f0c87bf502b92df951d90ef88c1c7d
    ├── [94md9[0m
    │   └── 2d079af6a7f276cc8d63dcf2549c03e7deb553
    ├── [94minfo[0m
    └── [94mpack[0m


.. code:: python

    print read_git_object('.git/objects/8a/dc8bf371d669242ea998f78f9916867cc6203c')

.. parsed-literal::

    blob 138 # The brain analysis script
    import numpy as np
    
    # Make brain data
    brain_size = (128, 128)
    random_data = np.random.normal(size=brain_size)
    


git commit - making the snapshot
================================

.. code:: python

    !git commit -m "First backup of my amazing idea"

.. parsed-literal::

    [master (root-commit) 1d7415e] First backup of my amazing idea
     3 files changed, 12 insertions(+)
     create mode 100644 nobel_prize.txt
     create mode 100644 stunning_figure.png
     create mode 100644 very_clever_analysis.py


In the commit above, we used the -m flag to specify a message at the
command line. If we don't do that, git will open the editor we specified
in our configuration above and require that we enter a message. By
default, git refuses to record changes that don't have a message to go
along with them (though you can obviously 'cheat' by using an empty or
meaningless string: git only tries to facilitate best practices, it's
not your nanny).

We are now expecting to have a .git object for the directory tree, and
for the commit.

.. code:: python

    print_tree('.git/objects')

.. parsed-literal::

    ├── [94m1d[0m
    │   └── 7415e14ef0d556a97630997644307942f7f703
    ├── [94m1e[0m
    │   └── 322f4e782df4dfe963eda96517886f4e39a454
    ├── [94m8a[0m
    │   └── dc8bf371d669242ea998f78f9916867cc6203c
    ├── [94m9f[0m
    │   └── fc311b29f0c87bf502b92df951d90ef88c1c7d
    ├── [94md9[0m
    │   └── 2d079af6a7f276cc8d63dcf2549c03e7deb553
    ├── [94minfo[0m
    └── [94mpack[0m


Here's the tree:

.. code:: python

    print read_git_object('.git/objects/1e/322f4e782df4dfe963eda96517886f4e39a454')

.. parsed-literal::

    tree 141 100644 nobel_prize.txt �-����v̍c��T��޵S100644 stunning_figure.png ��1)��{��-�Q���
    }100644 very_clever_analysis.py �܋�q�i$.������|� <


These are in fact the file permissions, the filenames, and a binary form
of the file hashes. Git will read this in a more friendly form for us:

.. code:: python

    !git ls-tree 1e322f4

.. parsed-literal::

    100644 blob d92d079af6a7f276cc8d63dcf2549c03e7deb553	nobel_prize.txt
    100644 blob 9ffc311b29f0c87bf502b92df951d90ef88c1c7d	stunning_figure.png
    100644 blob 8adc8bf371d669242ea998f78f9916867cc6203c	very_clever_analysis.py


git log - what are the commits so far?
======================================

.. code:: python

    !git log

.. parsed-literal::

    [33mcommit 1d7415e14ef0d556a97630997644307942f7f703[m
    Author: Matthew Brett <matthew.brett@gmail.com>
    Date:   Thu May 2 22:04:55 2013 -0700
    
        First backup of my amazing idea


.. code:: python

    !git log --parents

.. parsed-literal::

    [33mcommit 1d7415e14ef0d556a97630997644307942f7f703[m
    Author: Matthew Brett <matthew.brett@gmail.com>
    Date:   Thu May 2 22:04:55 2013 -0700
    
        First backup of my amazing idea


Why are these two outputs the same?

git branch - which branch are we on?
====================================

We haven't covered branches yet. Branches are bookmarks. They label the
commit we are on at the moment, and they track the commits as we do new
ones.

The default branch for git is called ``master``. Git creates it
automatically when you do your first commit.

.. code:: python

    !git branch

.. parsed-literal::

    * [32mmaster[m


.. code:: python

    !git branch -v

.. parsed-literal::

    * [32mmaster[m 1d7415e First backup of my amazing idea


.. code:: python

    !ls .git/refs/heads

.. parsed-literal::

    master


.. code:: python

    !cat .git/refs/heads/master

.. parsed-literal::

    1d7415e14ef0d556a97630997644307942f7f703


git diff - what has changed?
============================

Let's do a little bit more work... Again, in practice you'll be editing
the files by hand, here we do it via shell commands for the sake of
automation (and therefore the reproducibility of this tutorial!)

.. code:: python

    !echo "\nThe charts are very impressive\n" >> nobel_prize.txt

And now we can ask git what is different:

.. code:: python

    !git diff

.. parsed-literal::

    [1mdiff --git a/nobel_prize.txt b/nobel_prize.txt[m
    [1mindex d92d079..47b7547 100644[m
    [1m--- a/nobel_prize.txt[m
    [1m+++ b/nobel_prize.txt[m
    [36m@@ -4,3 +4,6 @@[m [mThe brain is just a set of random numbers[m
     We have discovered that the brain is a set of random numbers.[m
     [m
     We have charts and graphs to back us up.[m
    [32m+[m
    [32m+[m[32mThe charts are very impressive[m
    [41m+[m


You need to ``git add`` a file to put it into the staging area
==============================================================

Remember that git only commits stuff that has been added to the staging
area.

At the moment we have changes that have not been staged:

.. code:: python

    !git status

.. parsed-literal::

    # On branch master
    # Changes not staged for commit:
    #   (use "git add <file>..." to update what will be committed)
    #   (use "git checkout -- <file>..." to discard changes in working directory)
    #
    #	[31mmodified:   nobel_prize.txt[m
    #
    no changes added to commit (use "git add" and/or "git commit -a")


If we try and do a commit, git will tell us there is nothing to commit,
because nothing has been staged:

.. code:: python

    !git commit

.. parsed-literal::

    # On branch master
    # Changes not staged for commit:
    #   (use "git add <file>..." to update what will be committed)
    #   (use "git checkout -- <file>..." to discard changes in working directory)
    #
    #	[31mmodified:   nobel_prize.txt[m
    #
    no changes added to commit (use "git add" and/or "git commit -a")


The cycle of git virtue: work, commit, work, commit, ...
========================================================

.. code:: python

    !git status

.. parsed-literal::

    # On branch master
    # Changes not staged for commit:
    #   (use "git add <file>..." to update what will be committed)
    #   (use "git checkout -- <file>..." to discard changes in working directory)
    #
    #	[31mmodified:   nobel_prize.txt[m
    #
    no changes added to commit (use "git add" and/or "git commit -a")


.. code:: python

    !git add nobel_prize.txt
.. code:: python

    !git status

.. parsed-literal::

    # On branch master
    # Changes to be committed:
    #   (use "git reset HEAD <file>..." to unstage)
    #
    #	[32mmodified:   nobel_prize.txt[m
    #


.. code:: python

    !git commit -m "Fruit of enormous thought"

.. parsed-literal::

    [master ceda705] Fruit of enormous thought
     1 file changed, 3 insertions(+)


Remember branches?

.. code:: python

    !cat .git/refs/heads/master

.. parsed-literal::

    ceda7056aba330314aa219f7facbb00eb1a03248


git log revisited
=================

First, let's see what the log shows us now:

.. code:: python

    !git log

.. parsed-literal::

    [33mcommit ceda7056aba330314aa219f7facbb00eb1a03248[m
    Author: Matthew Brett <matthew.brett@gmail.com>
    Date:   Thu May 2 22:04:59 2013 -0700
    
        Fruit of enormous thought
    
    [33mcommit 1d7415e14ef0d556a97630997644307942f7f703[m
    Author: Matthew Brett <matthew.brett@gmail.com>
    Date:   Thu May 2 22:04:55 2013 -0700
    
        First backup of my amazing idea


.. code:: python

    !git log --parents

.. parsed-literal::

    [33mcommit ceda7056aba330314aa219f7facbb00eb1a03248 1d7415e14ef0d556a97630997644307942f7f703[m
    Author: Matthew Brett <matthew.brett@gmail.com>
    Date:   Thu May 2 22:04:59 2013 -0700
    
        Fruit of enormous thought
    
    [33mcommit 1d7415e14ef0d556a97630997644307942f7f703[m
    Author: Matthew Brett <matthew.brett@gmail.com>
    Date:   Thu May 2 22:04:55 2013 -0700
    
        First backup of my amazing idea


Making log output more pithy
============================

Sometimes it's handy to see a very summarized version of the log:

.. code:: python

    !git log --oneline --topo-order --graph

.. parsed-literal::

    * [33mceda705[m Fruit of enormous thought
    * [33m1d7415e[m First backup of my amazing idea


Git supports *aliases:* new names given to command combinations. Let's
make this handy shortlog an alias, so we only have to type ``git slog``
and see this compact log:

.. code:: python

    # We create our alias (this saves it in git's permanent configuration file):
    !git config --global alias.slog "log --oneline --topo-order --graph"
    
    # And now we can use it
    !git slog

.. parsed-literal::

    * [33mceda705[m Fruit of enormous thought
    * [33m1d7415e[m First backup of my amazing idea


``git mv`` and ``rm``: moving and removing files
================================================

While ``git add`` is used to add files to the list git tracks, we must
also tell it if we want their names to change or for it to stop tracking
them. In familiar Unix fashion, the ``mv`` and ``rm`` git commands do
precisely this:

.. code:: python

    !git mv very_clever_analysis.py slightly_dodgy_analysis.py
    !git status

.. parsed-literal::

    # On branch master
    # Changes to be committed:
    #   (use "git reset HEAD <file>..." to unstage)
    #
    #	[32mrenamed:    very_clever_analysis.py -> slightly_dodgy_analysis.py[m
    #


Note that these changes must be committed too, to become permanent! In
git's world, until something has been committed, it isn't permanently
recorded anywhere.

.. code:: python

    !git commit -m "I like this new name better"

.. parsed-literal::

    [master 01df2e1] I like this new name better
     1 file changed, 0 insertions(+), 0 deletions(-)
     rename very_clever_analysis.py => slightly_dodgy_analysis.py (100%)


.. code:: python

    !git slog

.. parsed-literal::

    * [33m01df2e1[m I like this new name better
    * [33mceda705[m Fruit of enormous thought
    * [33m1d7415e[m First backup of my amazing idea


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

.. code:: python

    !cat .git/HEAD

.. parsed-literal::

    ref: refs/heads/master


.. code:: python

    !cat .git/refs/heads/master

.. parsed-literal::

    01df2e1271fe12e0586f3a3876a567c684d6ce9b


.. code:: python

    !git branch -v

.. parsed-literal::

    * [32mmaster[m 01df2e1 I like this new name better


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

.. code:: python

    !git status
    !ls

.. parsed-literal::

    # On branch master
    nothing to commit (working directory clean)
    nobel_prize.txt            slightly_dodgy_analysis.py stunning_figure.png


We are now going to try two different routes of development: on the
``master`` branch we will add one file and on the ``experiment`` branch,
which we will create, we will add a different one. We will then merge
the experimental branch into ``master``.

.. code:: python

    !git branch experiment

What just happened? We made a branch, which is a pointer to this same
commit:

.. code:: python

    !ls .git/refs/heads

.. parsed-literal::

    experiment master


.. code:: python

    !git branch -v

.. parsed-literal::

      experiment[m 01df2e1 I like this new name better
    * [32mmaster    [m 01df2e1 I like this new name better


.. code:: python

    !cat .git/refs/heads/experiment

.. parsed-literal::

    01df2e1271fe12e0586f3a3876a567c684d6ce9b


How do we start working on this branch ``experiment`` rather than
``master``?

git checkout - set the current branch, set the working tree from a commit
=========================================================================

Up until now we have been on the ``master`` branch. When we make a
commit, the ``master`` branch pointer (``.git/refs/heads/master``) moves
up to track our most recent commit.

``git checkout`` can switch us to using another branch:

.. code:: python

    !git checkout experiment

.. parsed-literal::

    Switched to branch 'experiment'


What just happened?

.. code:: python

    !git branch -v

.. parsed-literal::

    * [32mexperiment[m 01df2e1 I like this new name better
      master    [m 01df2e1 I like this new name better


.. code:: python

    !cat .git/HEAD

.. parsed-literal::

    ref: refs/heads/experiment


As we'll see later, ``git checkout somebranch`` also sets the contents
of the working tree to match the commit contents for ``somebranch``. In
this case the commits for ``master`` and ``experiment`` are currently
the same, so we don't change the working tree at all.

Now let's do some changes on our ``experiment`` branch:

.. code:: python

    !echo "Some crazy idea" > experiment.txt
    !git add experiment.txt
    !git commit -m "Trying something new"
    !git slog

.. parsed-literal::

    [experiment b83cd47] Trying something new
     1 file changed, 1 insertion(+)
     create mode 100644 experiment.txt
    * [33mb83cd47[m Trying something new
    * [33m01df2e1[m I like this new name better
    * [33mceda705[m Fruit of enormous thought
    * [33m1d7415e[m First backup of my amazing idea


Notice we have a new file called ``experiment.txt`` in this branch:

.. code:: python

    !ls

.. parsed-literal::

    experiment.txt             nobel_prize.txt            slightly_dodgy_analysis.py stunning_figure.png


The ``experiment`` branch has now moved:

.. code:: python

    !cat .git/refs/heads/experiment

.. parsed-literal::

    b83cd47540cb7dbd7d16292d8a35417f031716f9


git checkout again - reseting the working tree
==============================================

If ``somewhere`` is a branch name, then ``git checkout somewhere``
selects ``somewhere`` as the current branch. It also resets the working
tree to match the working tree for that commit.

.. code:: python

    !git checkout master
    !cat .git/HEAD

.. parsed-literal::

    Switched to branch 'master'
    ref: refs/heads/master


We're back to the working tree as of the ``master`` branch;
``experiment.txt`` has gone now.

.. code:: python

    !ls

.. parsed-literal::

    nobel_prize.txt            slightly_dodgy_analysis.py stunning_figure.png


Meanwhile we do some more work on master:

.. code:: python

    !git slog

.. parsed-literal::

    * [33m01df2e1[m I like this new name better
    * [33mceda705[m Fruit of enormous thought
    * [33m1d7415e[m First backup of my amazing idea


.. code:: python

    !echo "All the while, more work goes on in master..." >> nobel_prize.txt
    !git add nobel_prize.txt
    !git commit -m "The mainline keeps moving"
    !git slog

.. parsed-literal::

    [master 5c436d0] The mainline keeps moving
     1 file changed, 1 insertion(+)
    * [33m5c436d0[m The mainline keeps moving
    * [33m01df2e1[m I like this new name better
    * [33mceda705[m Fruit of enormous thought
    * [33m1d7415e[m First backup of my amazing idea


.. code:: python

    !ls

.. parsed-literal::

    nobel_prize.txt            slightly_dodgy_analysis.py stunning_figure.png


Now let's do the merge

.. code:: python

    !git merge experiment -m "Merge in the experiment"

.. parsed-literal::

    Merge made by the 'recursive' strategy.
     experiment.txt | 1 [32m+[m
     1 file changed, 1 insertion(+)
     create mode 100644 experiment.txt


.. code:: python

    !git slog

.. parsed-literal::

    *   [33mb444163[m Merge in the experiment
    [31m|[m[32m\[m  
    [31m|[m * [33mb83cd47[m Trying something new
    * [32m|[m [33m5c436d0[m The mainline keeps moving
    [32m|[m[32m/[m  
    * [33m01df2e1[m I like this new name better
    * [33mceda705[m Fruit of enormous thought
    * [33m1d7415e[m First backup of my amazing idea


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

.. code:: python

    !git branch trouble
    !git checkout trouble
    !echo "This is going to be a problem..." >> experiment.txt
    !git add experiment.txt
    !git commit -m"Changes in the trouble branch"

.. parsed-literal::

    Switched to branch 'trouble'
    [trouble 6921250] Changes in the trouble branch
     1 file changed, 1 insertion(+)


And now we go back to the master branch, where we change the *same*
file:

.. code:: python

    !git checkout master
    !echo "More work on the master branch..." >> experiment.txt
    !git add experiment.txt
    !git commit -m"Mainline work"

.. parsed-literal::

    Switched to branch 'master'
    [master 1ebca55] Mainline work
     1 file changed, 1 insertion(+)


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

.. code:: python

    !git config merge.conflictstyle diff3

So now let's see what happens if we try to merge the ``trouble`` branch
into ``master``:

.. code:: python

    !git merge trouble -m "Unlikely this one will work"

.. parsed-literal::

    Auto-merging experiment.txt
    CONFLICT (content): Merge conflict in experiment.txt
    Automatic merge failed; fix conflicts and then commit the result.


Let's see what git has put into our file:

.. code:: python

    !cat experiment.txt

.. parsed-literal::

    Some crazy idea
    <<<<<<< HEAD
    More work on the master branch...
    ||||||| merged common ancestors
    =======
    This is going to be a problem...
    >>>>>>> trouble


Read this as:

-  Common ancestor (between ``||``... and ``==``) has nothing;
-  ``HEAD`` - the current branch - (between ``<<``... and ``||``) adds
   ``More work on the master branch...``;
-  the ``trouble`` branch (between ``==``... and ``>>``...) adds
   ``This is going to be a problem...``.

At this point, we go into the file with a text editor, decide which
changes to keep, and make a new commit that records our decision.

I'll do the edits by writing the file I want directly in this case:

.. code:: python

    %%file experiment.txt
    Some crazy idea
    More work on the master branch...
    This is going to be a problem...

.. parsed-literal::

    Overwriting experiment.txt


I've now made the edits. I decided that both pieces of text were useful,
but integrated them with some changes:

.. code:: python

    !git status

.. parsed-literal::

    # On branch master
    # You have unmerged paths.
    #   (fix conflicts and run "git commit")
    #
    # Unmerged paths:
    #   (use "git add <file>..." to mark resolution)
    #
    #	[31mboth modified:      experiment.txt[m
    #
    no changes added to commit (use "git add" and/or "git commit -a")


Let's then make our new commit:

.. code:: python

    !git add experiment.txt
    !git commit -m "Completed merge of trouble, fixing conflicts along the way"
    !git slog

.. parsed-literal::

    [master 51fd6ff] Completed merge of trouble, fixing conflicts along the way
    *   [33m51fd6ff[m Completed merge of trouble, fixing conflicts along the way
    [31m|[m[32m\[m  
    [31m|[m * [33m6921250[m Changes in the trouble branch
    * [32m|[m [33m1ebca55[m Mainline work
    [32m|[m[32m/[m  
    *   [33mb444163[m Merge in the experiment
    [33m|[m[34m\[m  
    [33m|[m * [33mb83cd47[m Trying something new
    * [34m|[m [33m5c436d0[m The mainline keeps moving
    [34m|[m[34m/[m  
    * [33m01df2e1[m I like this new name better
    * [33mceda705[m Fruit of enormous thought
    * [33m1d7415e[m First backup of my amazing idea


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


.. include:: links_names.inc
