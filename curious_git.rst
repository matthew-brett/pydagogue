.. check with make doctest

################################
The curious coder's guide to git
################################

*****************
git - love - hate
*****************

I've used git now for a long time.  I think it is a masterpiece of design, I
use it all day every day and I just can't imagine what it would be like not to
use it. So, no question, I *love* git.

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

But some people hate git.  Really *hate* it. They find it confusing and
error prone and it makes them angry.  Why are there such different views?

I think the reason some people hate git, is because they don't yet understand
it.  I reason I can say this without being patronizing is because I went
through something similar myself.

When I first started using git, I found it uncomfortable.  I could see it was
very powerful, but I sometimes got lost and stuck and had to Google for a set
of magic commands to get me out of trouble.  I once accidentally made a huge
mess of our project's main repository by running a command I didn't
understand. Git often made me feel stupid.  It felt like a prototype racecar
with a badly designed dashboard that was just about to blow a tire or an
engine and take me off the road.

Then, one day, I read the `git parable`_.  The git parable is a little story
about a developer trying to work out how to make a version control system.  It
gradually builds up from copying whole directories of files to something very
much like git.  I didn't understand it all right away, but as soon as I read
that page, the light-bulb went on - I got git.  I suddenly started to feel
comfortable.  I knew for sure I could work out why git worked the way it did.
I could see that it must be possible to do complicated and powerful
things, and I could work out how to do them.

Reading the git parable took me about 45 minutes, but those 45 minutes changed
me from an unhappy git user to someone who uses git often every day, but,
happily, knowing that I have the right tool for the job.

So, my experience tells me that to use git |--| yes *use* git |--| you need to
spend the short amount of time it takes to *understand* git.  You don't
believe me, or you think that I'm a strange kind of person not like you who
probably likes writing their own operating systems. Not so - the insight I'm
describing comes up over and over.  From `understanding git conceptually
<http://www.sbf5.com/~cduan/technical/git>`_:

    When I first started using Git, I read plenty of tutorials, as well as the
    user manual. Though I picked up the basic usage patterns and commands, I
    never felt like I grasped what was going on “under the hood,” so to speak.
    Frequently this resulted in cryptic error messages, caused by my random
    guessing at the right command to use at a given time. These difficulties
    worsened as I began to need more advanced (and less well documented)
    features.

Here's a quote from the `pro git book <http://git-scm.com/book>`_ by Scott
Chacon.  The git book is a standard reference that is hosted on the main git
website.

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

So |--| have no truck with people who try and tell you that you can just use
git and that you don't need the `deep shit`_. You *do* need the deep shit, but
the deep shit isn't that deep, and it will take you an hour of your time to
get all of it.  Then I'm betting that you'll see that the alchemist has
succeeded at last, and the |--| er |--| lead has finally turned into gold.

.. _deep:
.. _deep shit: http://rogerdudler.github.io/git-guide

So |--| please |--| invest a couple of hours of your life to understand this
stuff.  Concentrate, go slowly, make sure you get it. In return for a couple
of hours, you will get many happy years for which git will appear in its true
form, both beautiful and useful.

The one thing about git you really need to understand
=====================================================

git is not really a "Version Control System". It is better described
as a "Content Management System", that turns out to be really good for
version control.

I'll say that again.  Git is a content management system.  To quote from the
`root page of the git manual <http://git-scm.com/docs/git.html>`_: "git - the
stupid content tracker".

The reason that this is important is that git thinks in a very simple way
about files and directories.  You will ask git to keep snapshots of files in a
directory, and it does just this; it stores snapshots of the files, so you can
go back to them later.

Here is a story where we develop a very simple system for storing file
snapshots.  We soon find it starts to look just like git.

****************
A familiar story
****************

To understand why git does what it does, we first need to think about what a
content manager should do, and why we would want one.

If you've read the `git parable`_ (please do), then you'll recognize many of
the ideas.  Why?  Because they are good ideas, worthy of re-use.

As in the `git parable`_, we will try and design our own content manager, and
then see what git has to say.

(If you don't mind reading some Python code, and more jokes, then also try my
:doc:`foundation` page).

While we are designing our own content management system, we will do a lot of
stuff longhand, to show how things work.  When we get to git, we will find it
does these tasks for us.

The story so far...
===================

You are writing a breakthrough paper showing that you can explain how the
brain works by careful processing of some interesting data.  You've got the
analysis script, the data file and a figure for the paper.  These are all in a
directory modestly named ``nobel_prize``.

You can get this, the first draft, by downloading and unzipping
:download:`nobel_prize </np-versions/nobel_prize.zip>`.

.. workrun::
    :hide:

    # clean up old files from previous doc run
    rm -rf nobel_prize repos .gitconfig
    mkdir nobel_prize
    cp ../np-versions/work1/* nobel_prize

.. prizevar:: np_versions
    :omit_link:

    echo "../../np-versions"

Here's the current contents of our ``nobel_prize`` directory:

.. prizevar:: np_tools
    :omit_link:

    echo "../../np-tools"

.. prizevar:: np_tree
    :omit_link:

    echo "{{ np_tools }}/show_tree"

.. prizeout::

    # Show directory contents as tree
    {{ np_tree }}

The dog ate my results
======================

You've been working on this study for a while.

At first, you were very excited with the results. You ran the script, made the
figure, and the figure looked good.  That's the figure we currently have in
``nobel_prize`` directory. You took this figure to your advisor, Josephine.
She was excited too. You get ready to publish in Science.

You've done a few changes to the script and figure since then.  Today you
finished cleaning up for the Science paper, and reran the analysis, and it
doesn't quite the same. You go to see Josephine. She says "It used to look
better than that". That's what you think too. But:

* **Did it really look different before?**
* If it did, **what caused the change in the figure?**

Deja vu all over again
======================

Given you are so clever and you have discovered how the brain works, it is
really easy for you to leap in your time machine, and go back two weeks to
start again.

What are you going to do differently this time?

Gitwards 1: make regular snapshots
==================================

You decide to make your own content management system.  It's the simplest
thing that could possibly work, so you call it the "Simple As Possible"
system, or SAP for short.

Every time you finish doing some work on your paper, you make a snapshot
of the analysis directory.

The snapshot is a copy of all the files in the working directory.

First you make a directory called ``working``, and move your files to that
directory:

.. prizerun::
    :hide:
    :allow-fail:

    mkdir working
    mv * working

.. prizeout::

    {{ np_tree }}

When you've finished work for the day, you make a snapshot of the directory
containing the files you are working on.  The snapshot is just a copy of your
working directory:

.. prizerun::
    :hide:

    cp -r working snapshot_1

.. prizeout::

    {{ np_tree }}

You are going to do this every day you work on the project.

On the second day, you add your first draft of the paper, ``nobel_prize.md``.
You can download this ground-breaking work at :download:`nobel_prize.md
</np-versions/work2/nobel_prize.md>`.

.. prizerun::
    :hide:

    cp {{ np_versions }}/work2/nobel_prize.md working

.. prizeout::

    {{ np_tree }}

At the end of the day you make your second snapshot:

.. prizerun::
    :hide:

    cp -r working snapshot_2

.. prizeout::

    {{ np_tree }}

On the third day, you did some edits to the analysis script, and refreshed the
figure by running the script.  You did a third snapshot.

.. prizerun::
    :hide:

    cp {{ np_versions }}/work3/* working
    cp -r working snapshot_3

.. prizeout::

    {{ np_tree }}

To make the directory listing more compact, I'll sometimes show only the
number of files / directories in a subdirectory.  For example, here's a
listing of the three snapshots, but only showing the contents of the third
snapshot:

.. prizeout::

    {{ np_tree }} --elide snapshot --unelide snapshot_3

Finally, on the fourth day, you make some more edits to the script, and you
add some references for the paper.

.. prizerun::
    :hide:

    cp {{ np_versions }}/work4/* working
    cp -r working snapshot_4

.. prizeout::

    {{ np_tree }} --elide snapshot --unelide snapshot_4

You are ready for your fateful meeting with Josephine.  Again she notices that
the figure is different from the first time you showed her.  This time you can
go and look in ``nobel_prize/snapshot_1`` to see if the figure really is
different.  Then you can go through the snapshots to see where the figure
changed.

You've already got a useful content management system, but you are going to
make it better.

.. note::

    We are already at the stage where we can define some `terms
    <https://www.kernel.org/pub/software/scm/git/docs/gitglossary.html>`_ that
    apply to our system and that will later apply to git:

    Commit
        A completed snapshot. For example, ``snapshot_1`` contains one commit.

    Working tree
        The files you are working on in ``nobel_prize/working``.

Gitwards 2: reminding yourself of what you did
==============================================

.. Add message.txt

Your experience tracking down the change in the figure makes you think that it
would be good to save a message with each snapshot (commit) to record the
commit date and something about what changes you made.  Next time you need
to track down when and why something changed, you can look at the message to
give yourself an idea of the changes in the commit.  That might save you
time when you want to narrow down where to look for problems.

So, for each commit, you write write a file called ``message.txt``. The
message for the first commit looks like this:

.. prizewrite:: snapshot_1/message.txt

    Date: April 1 2012, 14.30
    Author: I. M. Awesome
    Notes: First backup of my amazing idea

.. prizewrite:: snapshot_2/message.txt
    :hide:

    Date: April 2 2012, 18.03
    Author: I. M. Awesome
    Notes: Add first draft of paper

There is a similar ``messsage.txt`` file for each commit. For example,
here's the message for the third commit:

.. prizewrite:: snapshot_3/message.txt

    Date: April 3 2012, 11.20
    Author: I. M. Awesome
    Notes: Add another fudge factor

This third message is useful because it gives you a hint that this was where
you made the important change to the script and figure.

.. note::

    Commit message
        Information about a commit, including the author, date, time, and some
        information about the changes in the commit, compared to the previous
        commits.

Gitwards 3: breaking up work into chunks
========================================

.. the staging area

Now you are used to having the commit messages in ``message.txt``, you aren't
so pleased with your fourth commit.  You now prefer to break your changes up
into self-contained chunks of work, with a matching commit message.  But,
looking at your fourth commit, it looks like you included two separate chunks
of work:

.. prizewrite:: snapshot_4/message.txt
    :hide:

    Date: April 4 2012, 01.40
    Author: I. M. Awesome
    Notes: Change analysis and add references

You decide to break this commit into two separate commits:

* A commit with the changes to the analysis script and figure, but without
  the references;
* Another commit to add the references.

To do this kind of thing, you adapt the workflow. Each time you have done a
commit, you copy the contents of the commit to new directory called
``staging``. This directory will become the contents for your next commit.
You can add changes from your working tree by copying the changed file into
``staging``.  When ``staging`` contains the changes you want, you make the
commit by copying ``staging`` into its own commit directory.

To get started, first you delete the old ``snapshot_4``.  Next you replace the
contents of ``staging`` with the contents of ``snapshot_3``.  You already have
the two sets of changes ready to stage in ``working``.

.. prizerun::
    :hide:

    rm -rf snapshot_4
    rm -rf staging
    cp -r snapshot_3 staging
    rm staging/message.txt

.. prizeout::

    {{ np_tree }} --hasta snapshot_2

Call the ``staging`` directory |--| the **staging area**.  Your new sequence
for making a commit is:

* Make sure the contents of the last commit are in the staging area;
* Copy any changes for the next commit from the working tree to the staging
  area;
* Make the commit by taking a snapshot of the staging area.

We are doing this by hand, but later git will make this much more automatic.

First we copy the changes we want from the working tree to the staging area:

.. prizerun::

    cp working/clever_analysis.py staging
    cp working/fancy_figure.png staging

The staging directory (staging area) now contains the right files for the
first of your two commits.

Next you make a commit by copying the staging area to ``snapshot_4`` and
adding a message:

.. prizerun::
    :hide:

    cp -r staging snapshot_4

.. prizewrite:: snapshot_4/message.txt

    Date: April 4 2012, 01.40
    Author: I. M. Awesome
    Notes: Change parameters of analysis

This gives:

.. prizeout::

    {{ np_tree }} --hasta snapshot_3

To finish, you make the second of the two commits.  Remember the sequence:

* Make sure the contents of the last commit are in the staging area;
* Copy any changes for the next commit from the working tree to the staging
  area;
* Make the commit by taking a snapshot of the staging area.

The staging area already contains the contents of the last commit (now
``snapshot_4``).  You copy the rest of the changes to the staging area:

.. prizerun::

    cp working/references.bib staging

Finally, you do the commit by copying ``staging`` to ``snapshot_5``, and
adding a commit message:

.. prizerun::
    :hide:

    cp -r staging snapshot_5

.. prizewrite:: snapshot_5/message.txt

    Date: April 4 2012, 02.10
    Author: I. M. Awesome
    Notes: Add references

Now you have:

.. prizeout::

    {{ np_tree }} --hasta snapshot_4

Now we can add a new term to our vocabulary:

.. note::

    Staging area
        Temporary area that contains the contents of the next commit.  We copy
        changes from the working tree to the staging area to **stage** those
        changes.  We make the new **commit** from the contents of the
        **staging area**.

Gitwards 4: getting files from previous commits
===============================================

Remember that you found the figure had changed?

You also found that the problem was in the third commit.

Now you look back over the commits, you realize that your first draft of the
analysis script was correct, and you decide to restore that.

To do that, you will **checkout** the script from the first commit
(``snapshot_1``).  You also want to checkout the generated figure.

Following our new standard staging workflow, that means:

* Get the files you want from the old commit into the working directory, and
  the staging area;
* Make a new commit from the staging area.

For our simple SAP system, that looks like this:

.. prizerun::

    # Copy files from old commit to working tree
    cp snapshot_1/clever_analysis.py working
    cp snapshot_1/fancy_figure.png working

.. prizerun::

    # Copy files from working tree to staging area
    cp working/clever_analysis.py staging
    cp working/fancy_figure.png staging
    cp -r staging snapshot_6

Then do the commit by copying ``staging``, and add a message:

.. prizewrite:: snapshot_6/message.txt

    Date: April 5 2012, 18.40
    Author: I. M. Awesome
    Notes: Revert to first version of script and figure

This gives:

.. prizeout::

    {{ np_tree }} --elide snapshot_ --unelide "snapshot_(1|6)"

.. note::

    Checkout (a file)
        To **checkout** a file is to restore the copy of a file as stored in a
        particular commit.

Gitwards 5: two people working at the same time
===============================================

.. How to have unique ids for the commits / snapshots

One reason that git is so powerful is that it works very well when more than
one person is working on the files in parallel.

Josephine is impressed with your SAP content management system, and wants to
use it to make some edits to the paper.  She takes a copy of your
``nobel_prize`` directory to put on her laptop.

She goes away for a conference.

While she is away, you do some work on the analysis script, and regenerate the
figure, to make ``shapshot_7``:

.. prizerun::
    :hide:

    cp {{ np_versions }}/work7m/* working
    cp working/* staging
    cp -r staging snapshot_7

.. prizewrite:: snapshot_7/message.txt
    :hide:

    Date: April 6 2012, 11.03
    Author: I. M. Awesome
    Notes: More fun with fudge

.. prizeout::

    {{ np_tree }} --elide staging --hasta snapshot_6

Meanwhile, Josephine decides to work on the paper.  Following your procedure,
she makes a commit herself.

What should Josephine's commit directory be called?

She could call it ``snapshot_7``, but then, when she gets back to the lab, and
gives you her ``nobel_prize`` directory, her copy of ``nobel_prize`` and yours
will both have a ``snapshot_7`` directory, but they will be different.  It
would be easy to copy Josephine's directory over yours or yours over
Josephine's, and lose the work.

For the moment, you decide that Josephine will attach her name to the commit
directory, to make it clear this is her snapshot.  So, she makes her commit
into the directory ``snapshot_7_josephine``.  When she comes back from the
conference, you copy her ``snapshot_7_josephine`` into your ``nobel_prize``
directory:

.. prizerun::
    :hide:

    cp -r snapshot_6 snapshot_7_josephine
    cp -r {{ np_versions }}/work7j/* snapshot_7_josephine

.. prizewrite:: snapshot_7_josephine/message.txt
    :hide:

    Date: April 6 2012, 14.30
    Author: J. S. Rightway
    Notes: Expand the introduction

.. prizeout::

    {{ np_tree }} --elide staging --hasta snapshot_6

After the copy, you still have your own copy of the working tree, without
Josephine's changes to the paper. You want to combine your changes with her
changes.  To do this you do a **merge** by copying her changes to the paper
into the working directory.

.. prizerun::

    # Get Josephine's changes to the paper
    cp snapshot_7_josephine/nobel_prize.md working

Now you do a commit with these merged changes, by copying them into the
staging area, and thence to ``snapshot_8``, with a suitable message:

.. prizerun::
    :hide:

    cp working/* staging
    cp -r staging snapshot_8

.. prizewrite:: snapshot_8/message.txt
    :hide:

    Date: April 7 2012, 15.03
    Author: I. M. Awesome
    Notes: Merged Josephine's changes

.. prizeout::

    {{ np_tree }} --hasta "snapshot_7$"

This new commit is the result of a merge, and therefore it is a **merge
commit**.

.. note::

    Merge
        To make a new **merge commit** by combining changes from two (or
        more) commits.

Gitwards 6: how should we name our commit directories?
======================================================

You like your new system, and so does Josephine, but you don't much like your
solution of adding Josephine's name to the commit directory |--| as in
``snapshot_7_josephine``.  There might be lots of people working on this
paper.  With your naming system, you have to give out a unique name to each
person working on ``nobel_prize``.  As you think about this problem, you begin
to realize that what you want is a system for giving each commit directory a
unique name, that comes from the contents of the commit.  This is where you
starting thinking about **hashes**.

A diversion on cryptographic hashes
===================================

This section describes "Cryptographic hashes". These will give us an excellent
way to name our snapshots.  Later we will see that they are central to the way
that git works.

See : `Wikipedia on hash
functions <http://en.wikipedia.org/wiki/Cryptographic_hash_function>`__.

A *hash* is the result of running a *hash function* over a block of
data. The hash is a fixed length string that is the characteristic
*fingerprint* of that exact block of data.  One common hash function is called
SHA1.  Let's run this via the command line:

.. desktoprun::

    # Make a file with a single line of text
    echo "git is a rude word in UK English" > git_is_rude
    # Show the SHA1 hash
    shasum git_is_rude

Not too exciting so far. However, the rather magical nature of this string is
not yet apparent. This SHA1 hash is a *cryptographic* hash because:

* the hash value is (almost) unique to this exact file contents, and
* it is (almost) impossible to find some other file contents with the same
  hash.

By "almost impossible" I mean that finding a file with the same hash is
roughly the same level of difficulty as trying something like $16^40$
different files (where 16 is the number of different hexadecimal digits, and
40 is the length of the SHA1 string).

In other words, there is no practical way for you to find another file with
different contents that will give the same hash.

For example, a tiny change in the string makes the hash completely different.
Here I've just added a full stop at the end:

.. desktoprun::

    echo "git is a rude word in UK English." > git_is_rude_stop
    shasum git_is_rude_stop

So, if you give me some data, and I calculate the SHA1 hash value, and it
comes out as ``30ad6c360a692c1fe66335bb00d00e0528346be5``, then I can be very
sure that the data you gave me was exactly the ASCII string "git is a rude
word in UK English".

.. _naming-from-hashes:

Gitwards 7: naming commits from hashes
======================================

Now you have hashing under your belt, maybe it would be a good way of making a
unique name for the commits.  You could take the SHA1 hash for the
``message.txt`` for each commit, and use that SHA1 hash as the name for the
commit directory.  Because each message has the date and time and author and
notes, it's very unlikely that any two ``message.txt`` files will be the same.
Here are the hashes for the current ``message.txt`` files:

.. prizerun::

    # Show the SHA1 hash values for each message.txt
    shasum snapshot*/message.txt

.. prizevar:: snapshot_1_sha

    shasum snapshot_1/message.txt | awk '{print $1}'

.. prizevar:: snapshot_2_orig_sha

    shasum snapshot_2/message.txt | awk '{print $1}'

For example you could rename the ``snapshot_1`` directory to
|snapshot_1_sha|, then rename ``snapshot_2`` to |snapshot_2_orig_sha| and so
on:

.. prizeout::

    {{ np_tools }}/mv_shas.sh
    snapshot_1=$({{ np_tools }}/name2sha.sh snapshot_1)
    {{ np_tree }} --elide "\S+" --unelide "$snapshot_1"

The problem you have now is that the directory names no longer tell you the
sequence of the commits, so you can't tell that ``snapshot_2`` (now
|snapshot_2_orig_sha|) follows ``snapshot_1`` (now |snapshot_1_sha|).

OK |--| you scratch the renaming for now while you have a rethink.

.. prizeout::

    {{ np_tools }}/unmv_shas.sh
    {{ np_tree }} --elide "\S+" --unelide "snapshot_1"

You still want to rename the commit directories, from the ``message.txt``
hashes, but you need a way to store the sequence of commits, after you have
done this.

After some thought, you come up with a quite brilliant idea.  Each
``message.txt`` will point back to the previous commit in the sequence.  You
add a new field to ``messsage.txt`` called ``Parents``.
``snapshot_1/message.txt`` stays the same, because it has no parents:

.. prizerun::

    cat snapshot_1/message.txt

``snapshot_2/message.txt`` does change, because it now points back to
``snapshot_1``.  But, you're going to rename the snapshot directories, so you
want ``snapshot_2/message.txt`` to point back to the hash for
``snapshot_1/message.txt``, which we know is |snapshot_1_sha|:

.. prizerun::
    :hide:

    {{ np_tools }}/link_commits.py

.. prizerun::

    cat snapshot_2/message.txt

Now we've changed the contents and therefore the hash for
``snapshot_2/message.txt``.  The hash was |snapshot_2_orig_sha|, but now it
is:

.. prizerun::

    shasum snapshot_2/message.txt

We keep doing this procedure, for all the commits, modifying ``message.txt``
and recalculating the hash, until we come to ``snapshot_8``, the merge commit.
This commit is the result of merging two commits: ``snapshot_7`` and
``snapshot_7_josephine``.  You can record this information by putting *two*
parents into the ``Parents`` field of ``snapshot_8/message.txt``, being the
new hashes for ``snapshot_7/message.txt`` and
``snapshot_7_josephine/message.txt``:

.. prizerun::

    shasum snapshot_7/message.txt

.. prizerun::

    shasum snapshot_7_josephine/message.txt

.. prizerun::

    cat snapshot_8/message.txt

With the new ``Parents`` field, you have new hashes for all the
``message.txt`` files, except ``snapshot_1`` (that has no parent):

.. prizerun::

    shasum snapshot_*/message.txt

You can now rename your snapshot directories with the hash values, safe in the
knowledge that the ``message.txt`` files have the information about the commit
sequence:

.. prizerun::
    :hide:

    {{ np_tools }}/mv_shas.sh

.. prizeout::

    {{ np_tree }} --elide "\S+" --unelide "{{snapshot_1_sha}}"

.. note::

    Commit hash
        The hash value for the file containing the **commit message**.

Gitwards 8: the development history is a graph
==============================================

The commits are linked by the "Parents" field in the ``message.txt`` file.  We
can think of the commits in a graph, where the commits are the nodes, and the
links between the nodes come from the hashes in the "Parents" field.

.. workrun::
    :hide:

    cd ../generated
    ../tools/make_dot.py > snapshot_graph1.dot
    dot -Tpng -o snapshot_graph1.png snapshot_graph1.dot
    dot -Tpdf -o snapshot_graph1.pdf snapshot_graph1.dot

.. figure:: /generated/snapshot_graph1.*

    Graph of development history for your SAP content management system.  The
    most recent commit is at the top, the first commit is at the bottom.  Your
    commits are in blue, Josephine's are in pink.  Each commit label has the
    hash for the commit message, and the note in the ``message.txt`` file.

Gitwards 9: saving space with file hashes
=========================================

While you've been working on your system, you've noticed that your snapshots
are not efficient on disk space.  For example, every commit / snapshot has an
identical copy of the data ``expensive_data.csv``.  If you had bigger files or
a longer development history, this could be a problem.

.. prizevar:: snapshot_2_sha

    echo $({{ np_tools }}/name2sha.sh snapshot_2)

.. prizevar:: snapshot_3_sha

    echo $({{ np_tools }}/name2sha.sh snapshot_3)

.. prizevar:: snapshot_6_sha

    echo $({{ np_tools }}/name2sha.sh snapshot_6)

.. prizevar:: snapshot_8_sha

    echo $({{ np_tools }}/name2sha.sh snapshot_8)

Likewise, ``fancy_figure.png`` and ``clever_analysis.py`` are the same for the
first two commits, and then again when you reverted to that copy in
``snapshot_6`` (that is now commit |snapshot_6_sha|).

You can show these files are the same by checking their hash strings.  If
their hash strings are different, the files must be different.  All copies of
``expensive_data.csv`` have the same hash, and are therefore identical:

.. prizevar:: asterisk
    :omit_link:

    # Because * as in file system glob messes up syntax highlighting in vim
    echo "*"

.. prizerun::

    shasum {{ asterisk }}/expensive_data.csv

``fancy_figure.png`` is the same for the first two commits, changes for the
third commit, and reverts back to the same contents at the 6th commit:

.. prizerun::

    # First commit
    shasum {{ snapshot_1_sha }}/fancy_figure.png

.. prizerun::

    # Second commit
    shasum {{ snapshot_2_sha }}/fancy_figure.png

.. prizerun::

    # Third commit
    shasum {{ snapshot_3_sha }}/fancy_figure.png

.. prizerun::

    # Sixth commit
    shasum {{ snapshot_6_sha }}/fancy_figure.png

You wonder if there is a way to store each unique version of the file just
once, and make the commits point to the matching version.

First you make a new directory to store files generated from your commits:

.. prizerun::

    mkdir repo

Next you make a sub-directory to store the unique copies of the files in
commits:

.. prizerun::

    mkdir repo/objects

You play with the idea of calling these unique versions something like
``repo/objects/fancy_figure.png.v1``, ``repo/objects/fancy_figure.png.v2`` and
so on.  You would then need something like a text file called
``directory_listing.txt`` in the first commit directory to say that the file
``fancy_figure.png`` for this commit is available at
``repo/objects/fancy_figure.png.v1``.  This could be something like::

    # directory_listing.txt in first commit
    fancy_figure.png -> repo/objects/fancy_figure.png.v1

``directory_listing.txt`` for the second commit would point to the same file,
but the third commit would have something like::

    # directory_listing.txt in third commit
    fancy_figure.png -> repo/objects/fancy_figure.png.v2

You quickly realize this is going to get messy when you are working with other
people, because you may store ``repo/objects/fancy_figure.png.v3`` while
Josephine is also working on the figure, and is storing her own
``repo/objects/fancy_figure.png.v3``.  You need a unique file name for each
version of the file.

Now you have your second quite brilliant hashing idea.  Why not use the
**hash** of the file to make a unique file name?

For example, here are the hash values for the files in the first commit:

.. prizerun::

    shasum {{ snapshot_1_sha }}/*

.. prizevar:: fancy_figure_v1_sha

    shasum {{ snapshot_1_sha }}/fancy_figure.png | awk '{print $1}'

.. prizevar:: clever_analysis_v1_sha

    shasum {{ snapshot_1_sha }}/clever_analysis.py | awk '{print $1}'

.. prizevar:: expensive_data_sha

    shasum {{ snapshot_1_sha }}/expensive_data.csv | awk '{print $1}'

To store the unique copies, you copy each file in the first commit to
``repo/objects`` with a unique file name.  **The file name is the hash of the
file contents**.  For example, the hash for ``fancy_figure.png`` is
|fancy_figure_v1_sha|.  So, you do:

.. prizerun::

    cp {{ snapshot_1_sha }}/fancy_figure.png repo/objects/{{ fancy_figure_v1_sha }}

The hash values for ``clever_analysis.py`` and ``expensive_data.csv`` are
|clever_analysis_v1_sha| and |expensive_data_sha| respectively, so:

.. prizerun::

    cp {{ snapshot_1_sha }}/clever_analysis.py repo/objects/{{ clever_analysis_v1_sha }}
    cp {{ snapshot_1_sha }}/expensive_data.csv repo/objects/{{ expensive_data_sha }}

These hash values become the ``directory_listing.txt`` for the first commit:

.. prizerun::
    :hide:

    cd {{ snapshot_1_sha }}
    shasum * | grep -v 'message.txt' > directory_listing.txt

.. prizerun::

    cat {{ snapshot_1_sha }}/directory_listing.txt

Finally, you can delete ``fancy_figure.png``, ``clever_analysis.py`` and
``expensive_data.csv`` in the first commit directory, because you have them
backed up in ``repo/objects``.

So far you haven't gained anything much except some odd-looking filenames.
The payoff comes when you apply the same procedure to the second commit.  Here
are the hashes for the files in the second commit:

.. prizerun::

    shasum {{ snapshot_2_sha }}/*

.. prizevar:: nobel_prize_v1_sha

    shasum {{ snapshot_2_sha }}/nobel_prize.md | awk '{print $1}'

Remember that, in the second commit, all you did was add the first draft of
the paper as ``nobel_prize.md``.  So, all the other files in the second commit
(apart from ``message.txt`` that you are not storing) are the same as for the
first commit, and therefore have the same hash.  You already have these files
backed up in ``repo/objects`` so all you need to do is point
``directory_listing.txt`` at the original copies in ``repo/objects``.

For example, the hash for ``fancy_figure.png`` in the second commit is
|fancy_figure_v1_sha|.  When you are storing the files for the second commit
in ``repo/objects``, you notice that you already have a file
named |fancy_figure_v1_sha| in ``repo/objects``, so you do not copy it a
second time.  By checking the hashes for each file in the commit, you find
that the only file you are missing is the new file ``nobel_prize.md``.  This
has hash |nobel_prize_v1_sha|, so you do a single copy to ``repo/objects``:

.. prizerun::

    # Only one copy needed to store files in second commit
    cp {{ snapshot_2_sha }}/nobel_prize.md repo/objects/{{ nobel_prize_v1_sha }}

As before, we can make ``directory_listing.txt`` for the second commit by
recording the hashes of the files:

.. prizerun::
    :hide:

    cd {{ snapshot_2_sha }}
    shasum * | grep -v 'message.txt' > directory_listing.txt

.. prizerun::

    cat {{ snapshot_2_sha }}/directory_listing.txt

Before you start this procedure of moving the unique copies into
``repo/objects``, your whole ``nobel_prize`` directory is size:

.. prizerun::
    :hide:

    rm -rf repo/objects

.. prizerun::

    # Size of the contents of nobel_prize before moving to repo/objects
    du -hs .

When you run the procedure above on every commit, moving files to
``repo/objects``, you have this:

.. prizerun::
    :hide:

    {{ np_tools }}/to_repo_objects.py

.. prizeout::

    {{ np_tree }} --elide ize/working --elide staging

The whole ``nobel_prize`` directory is now smaller because you have no
duplicated files:

.. prizerun::

    # Size of the contents of nobel_prize after moving to repo/objects
    du -hs .

The advantage in size gets larger as your system grows, and you have more
duplicated files.

Gitwards 10: making the commits unique
======================================

.. hashing the directory listing; including hashes in the commit

Up in :ref:`naming-from-hashes` you used the hash of ``message.txt`` as a
nearly unique directory name for the commit.  Your thinking was that it was
very unlikely that any two commits would have the same author, date, time, and
note.  We have since added the ``Parents`` field to ``message.txt`` to make it
even more unlikely.  But |--| it could still happen.  You might be careless
and make another commit very quickly after the previous, and without a note.
You could even point back to the same parent.

You would like to be even more confident that the commit message is unique to
the commit, including the contents of the files in the commit.

You now have a way of doing this.   The ``directory_listing.txt`` files
contain a list of hashes and corresponding file names for this commit
(snapshot).  For example, here is ``directory_listing.txt`` for the first
commit:

.. prizerun::

    cat {{ snapshot_1_sha }}/directory_listing.txt

The contents of this file are (very nearly) unique to the contents of the
files in the snapshot.  If any of the files changed, then the hash of the file
would change and the corresponding line in ``directory_listing.txt`` would
change.  If you renamed the file, the name of the file would change and the
corresponding line in ``directory_listing.txt`` would change.

Now you know what to do.  You take a hash of the ``directory_listing.txt``
file:

.. prizerun::

    shasum {{ snapshot_1_sha }}/directory_listing.txt

.. prizerun::
    :hide:

    {{ np_tools }}/add_tree.py

You put this has into a new field in ``message.txt`` called ``Directory
hash:``:

.. prizeout::

    cat {{ snapshot_1_sha }}/message.txt

Now, if any file in the commit changes, ``directory_listing.txt`` will change,
and so its hash will change, and so ``message.txt`` will change.

Now you've added the ``Directory hash`` field to ``messsage.txt`` you have
also changed the hash values of the ``message.txt`` files.  Because you've
changed the hashes of the ``message.txt`` files, you go back through your
commits updating the parent hashes to the new ones, and renaming the commit
directories with the new hashes.  You end up with this:

.. prizerun::
    :hide:

    {{ np_tools }}/mv_shas.sh

.. workrun::
    :hide:

    cd ../generated
    ../tools/make_dot.py > snapshot_graph2.dot
    dot -Tpng -o snapshot_graph2.png snapshot_graph2.dot
    dot -Tpdf -o snapshot_graph2.pdf snapshot_graph2.dot

.. figure:: /generated/snapshot_graph2.*

    Development history graph with new hashes after adding directory hash
    field.

With your new system, if any two commits have the same ``message.txt`` then
they also have the same date, author, note, parents and file contents.  They
are therefore exactly the same commit.

.. note::

    The commit message is unique to the contents of the files in the snapshot
    (because of the directory hash) and unique to its previous history
    (because of the parent hash(es)).

Gitwards 11: away with the snapshot directories
===============================================

.. hashing the commits

You are reflecting on your idea about hashing the directory listing, and your
eye falls idly on the current directory tree of ``nobel_prize``:

.. prizevar:: snapshot_1_with_tree_sha

    echo $({{ np_tools }}/name2sha.sh {{ snapshot_1_sha }})

.. prizeout::

    {{ np_tree }} --elide ize/working --elide staging --elide repo/objects

It suddenly occurs to you |--| you can take the hash of each
``directory_listing.txt`` and move it into the ``repo/objects`` directory as
you did for the other files:

.. prizevar:: snapshot_1_tree_hash

    shasum {{ snapshot_1_with_tree_sha }}/directory_listing.txt | awk '{print $1}'

.. prizerun::

    shasum {{ snapshot_1_with_tree_sha }}/directory_listing.txt

.. prizerun::

    cp {{ snapshot_1_with_tree_sha }}/directory_listing.txt repo/objects/{{ snapshot_1_tree_hash }}

And you can do the same for the ``message.txt`` file:

.. prizerun::

    cp {{ snapshot_1_with_tree_sha }}/message.txt repo/objects/{{ snapshot_1_with_tree_sha }}

.. prizevar:: n_commits

    wc .names2sha | awk '{print $1}' 

There are |n_commits| commits, so |n_commits| x 2 new files with hash
filenames in ``repo/objects`` (a hashed copy of ``directory_listing.txt`` and
``message.txt`` for each commit).

Now you don't need the snapshot directories at all, because the hashed files
in ``repo/objects`` have all the information about the snapshots.

.. prizerun::
    :hide:

    ../../np-tools/move_snapshots.py

.. prizeout::

    {{ np_tree }} --elide ize/working --elide staging --elide repo/objects

.. note::

    In git as in your SAP content management system, a **repository
    directory** stores all the data from the snapshots.  In your case that
    directory is ``repo``.  For git, it will be a directory called ``.git``.

Gitwards 12: where am I?
========================

You have one last problem to face |--| where is your latest commit?

When your snapshot directory names had numbers, like ``snapshot_8``, you could
use the numbers to find the most recent commit.  Now all you have is a
directory called ``repo/objects`` with unhelpful file names made from hashes.
Which of these files has your latest commit?

You could write down the latest commit hash on a piece of paper, after you
make the commit, but this sounds like a job better done by a computer.

.. prizevar:: snapshot_8_with_tree_sha

    echo $({{ np_tools }}/name2sha.sh {{ snapshot_8_sha }})

.. prizerun::
    :hide:

    echo {{ snapshot_8_with_tree_sha }} > repo/my_bookmark

So, when you make a new commit, you store the hash for that commit in a file
called ``repo/my_bookmark``.  It is a text file with the hash string as
contents.  Your last commit was |snapshot_8_with_tree_sha|, so
``repo/my_bookmark`` has contents:

.. prizerun::

    cat repo/my_bookmark

You can imagine that, when Josephine is working on the same set of files, she
might want her own bookmark, maybe ``josephines_bookmark``.

.. note::

    We keep track of the latest commit in a particular sequence by storing the
    latest **commit hash** in a bookmark file.  In git this bookmark is called
    a **branch**.

*************************
From gitwards to gitworld
*************************

Now you have built your own content management system, you know how git works
|--| because it works in exactly the same way.  You will recognize hashes for
files, directories and commits, commits linked by reference to their parents,
the staging area, the ``objects`` directory, and bookmarks (branches).

Armed with this deep_ understanding, we retrace our steps to do the same
content management tasks in git.

Basic configuration
===================

We need to tell git our name and email address before we start.

Git will use this information to fill in the author information in each
**commit message**, so we don't have to type it out every time.

.. prizerun::

    git config --global user.name "Matthew Brett"
    git config --global user.email "matthew.brett@gmail.com"

The ``--global`` flag tells git to store this information in its default
configuration file for your user account.  On Unix (e.g. OSX and Linux) this
file is ``.gitconfig`` in your home directory.  Without the ``--global`` flag,
git only applies the configuration to the particular **repository** you are
working in.

Every time we make a commit, we need to type a commit message.  Git will open
our text editor for us to type the message, but first it needs to know what
text editor we prefer.  Set your own preferred text editor here::

    # gedit is a reasonable choice for Linux
    # "vi" is the default.
    git config --global core.editor gedit

We also turn on the use of color, which is very helpful in making the
output of git easier to read:

.. prizerun::

    git config --global color.ui "auto"

Getting help
============

.. prizerun::

    git help

Try ``git help add`` for an example.

.. note::

    The git help pages are famously hard to read if you don't know how git
    works. One purpose of this tutorial is to explain git in such a way that
    it will be easier to understand the help pages.

Initializing the repository directory
=====================================

We first set this ``nobel_prize`` directory to be version controlled with git.
We start off the working tree with the original files for the paper:

.. desktoprun::
    :hide:

    rm -rf nobel_prize
    cp ../nobel_prize.zip .
    mkdir nobel_prize
    cp ../np-versions/work1/* nobel_prize

.. note::

    I highly recommend you type along.  Why not download
    :download:`nobel_prize.zip </np-versions/nobel_prize.zip>` and unzip the
    files to make the same ``nobel_prize`` directory as I have here?

.. prizeout::

    {{ np_tree }}

To get started with git, create the git **repository directory** with ``git
init``:

.. desktoprun::

    cd nobel_prize
    git init

What happened when we did ``git init``? Just what we were expecting; we have a
new repository directory in ``nobel_prize`` called ``.git``

.. prizeout::

    {{ np_tree }} .git --elide hooks

The ``objects`` directory looks familiar.  It has exactly the same purpose as
it did for your SAP system.  At the moment it contains a couple of empty
directories, because we have not added any objects yet.

Updating terms for git
======================

Working directory
    The directory containing the files you are working on.  In our case this
    is ``nobel_prize``.  It contains the **repository directory**, named
    ``.git``.

Repository directory
    Directory containing all previous commits (snapshots) and git private
    files for working with commits.  The directory has name ``.git`` by
    default, and almost always in practice.

.. _git-add:

git add |--| put stuff into the staging area
============================================

In the next few sections, we will do our first commit (snapshot).

First we will put the files for the commit into the staging area.

The command to put files into the staging area is ``git add``.

First, we show ourselves that the **staging area** is empty. We haven't yet
discussed the git implementation of the staging area, but this command shows
us which files are in the staging area.

.. prizerun::

    git ls-files --stage

As expected, there are no files in the staging area yet.

.. note::

    ``git ls-files`` is a specialized command that you will not often need in
    your daily git life.  I'm using it here to show you how git works.

Now we do our add:

.. prizerun::

    git add clever_analysis.py

The git staging area
====================

It is time to think about what the staging area is, in git.  In your SAP
system, the staging area was a directory.  You also started off by using
directories to store commits (snapshots).  Later you found you could do
without the commit directories, because you could store the directory
structure in ``directory_listing.txt`` text files, and then copy these into
your ``repo/objects`` directory.

In git, the staging area is a single file called ``.git/index``.  This file
contains a directory listing that is the equivalent of the ``staging``
directory in SAP.  When we add a file to the staging area, git backs up the
file with its hash to ``.git/objects``, and then changes the directory listing
inside ``.git/index`` to point to this backup copy.

Now we have done the ``git add``, we expect that the new file will show up in
the staging area:

.. prizerun::

    git ls-files --stage

The output shows the hash of the backed up copy of ``clever_analysis.py``.

We can see this hashed backup file in ``.git/objects``:

.. prizeout::

    {{ np_tree }} .git/objects

The filename of the new file comes from the hash recorded in the staging area.
The first two digits of the hash form the directory name and the rest of the
digits are the filename [#git-object-dir]_.

Git objects
===========

Git objects are nearly as simple as the objects you were writing in your SAP.
The hash is not the hash of the raw file, but the raw file prepended with a
short housekeeping string.  See :doc:`reading_git_objects` for details.

We can see the contents of objects with the command ``git cat-file -p``.

.. prizevar:: analysis_1_hash

    git rev-parse :clever_analysis.py

.. prizerun::

    git cat-file -p {{ analysis_1_hash }}

.. note::

    I will use ``git cat-file -p`` to display the content of nearly raw git
    objects, to show the simplicity of git's internal model, but ``cat-file``
    is a specialized command that you won't use much in daily work.

Just as we expected, it is the current contents of the
``clever_analysis.py``.

The |analysis_1_hash| object is hashed, stored raw file.  Because the object
is a stored file rather than a stored directory listing text file or commit
message text file, git calls this type of object a **blob** for Binary Large
Object.  You can see the object from the object hash with the ``-t`` flag to
``git cat-file``:

.. prizerun::

    git cat-file -t {{ analysis_1_hash }}

Hash values can usually be abbreviated to seven characters
==========================================================

We only need to give git enough hash digits for git to identify the object
uniquely.  7 digits nearly always enough, as in:

.. prizevar:: sha_7

    echo "function sha_7 { echo \${1:0:7}; }; sha_7 "

.. prizevar:: analysis_1_hash_7

    {{ sha_7 }} {{ analysis_1_hash }}

.. prizerun::

    git cat-file -p {{ analysis_1_hash_7 }}

git status |--| showing the status of files in the working tree
===============================================================

The working tree is the contents of the ``nobel_prize`` directory, excluding
the ``.git`` repository directory.

``git status`` tells us about the relationship of the files in the working
tree to the repository and staging area.

We have done a ``git add`` on ``clever_analysis.py``, and that added the file
to the staging area.  We can see that this happened with ``git status``:

.. prizerun::

    git status

Sure enough, the output tells that ``new file: clever_analysis.py`` is in
the ``changes to be committed``.  It also tells us that the other two files in
the working directory are ``untracked``.

An untracked file is a file with a filename that has never been added to the
repository with ``git add``.  Until you do ``git add`` an untracked file, git
will ignore these files and assume you don't want to keep track of them.

Staging the other files with git add
====================================

We do want to keep track of the other files, so we stage them:

.. prizerun::

    git add fancy_figure.png
    git add expensive_data.csv
    git status

We have staged all three of our files.  We have three objects in
``.git/objects``:

.. prizeout::

    {{ np_tree }} .git/objects

git commit |--| making the snapshot
===================================

.. prizecommit:: commit_1_sha 2012-04-01 14:30:13

    git commit -m "First backup of my amazing idea"

.. note::

    In the line above, I used the ``-m`` flag to specify a message at the
    command line. If I had not done that, git would open the editor I
    specified in the ``git config`` step above and ask me to enter a message.
    I'm using the ``-m`` flag so the commit command runs without interaction
    in this tutorial, but in ordinary use, I virtually never use ``-m``, and I
    suggest you don't either.  Using the editor for the commit message allows
    you to write a more complete commit message, and gives feedback about the
    ``git status`` of the commit to remind you what you are about to do.

Following the logic of your SAP system, we expect that the action of making
the commit will generate two new files in ``.git/objects``, one for the
directory listing text file, and another for the commit message:

.. prizeout::

    {{ np_tree }} .git/objects

Here is the contents of the commit message text file for the new commit.  Git
calls this a **commit object**:

.. prizerun::

    git cat-file -p {{ commit_1_sha }}

.. prizerun::

    # What type of git object is this?
    git cat-file -t {{ commit_1_sha }}

As for SAP, the commit message file contains the hash for the directory tree
file (``tree``), the hash of the parent (``parent``) (but this commit has no
parents), the author, date and time, and the note.

Here's the contents of the directory listing text file for the new commit.
Git calls this **tree object**.

.. prizevar:: commit_1_tree_sha

    git rev-parse HEAD:./

.. prizerun::

    git cat-file -p {{ commit_1_tree_sha }}

.. prizerun::

    git cat-file -t {{ commit_1_tree_sha }}

Each line in the directory listing give the file permissions, the type of the
entry in the directory (where "tree" means a sub-directory, and "blob" means a
file), the file hash, and the file name (see :ref:`git-object-types`).

git log |--| what are the commits so far?
=========================================

.. prizerun::

    git log

Notice that git log identifies each commit with its hash.  As we saw above,
the hash for our commit was |commit_1_sha|.

We can also ask to the see the parents of each commit in the log:

.. prizerun::

    git log --parents

Why are the output of ``git log`` and ``git log --parents`` the same in this
case? (answer [#no-parents]_).

git branch - which branch are we on?
====================================

Branches are bookmarks. They associate a name (like "my_bookmark" or "master")
with a commit (such as |commit_1_sha|).

The default branch (bookmark) for git is called ``master``. Git creates it
automatically when we do our first commit.

.. prizerun::

    git branch

Asking for more verbose detail shows us that the branch is pointing to a
particular commit (where the commit is given by a hash):

.. prizerun::

    git branch -v

A branch is nothing but a name that points to a commit.  In fact, git stores
branches as we did in SAP, as tiny text files, where the filename is the name
of the branch, and the contents is the hash of the commit that it points to:

.. prizerun::

    ls .git/refs/heads

.. prizerun::

    cat .git/refs/heads/master

We will soon see that, if we are working on a branch, and we do a commit, then
git will update the branch to point to the new commit.

A second commit
===============

In our second commit, we will add the first draft of the Nobel prize paper.
As before, you can download this from
:download:`nobel_prize.md </np-versions/work2/nobel_prize.md>`.  If you are
typing along, download ``nobel_prize.md`` to the ``nobel_prize`` directory.

This git repository has not need the filename ``nobel_prize.md`` before, so
``git status`` identifies this file as **untracked**:

.. prizerun::
    :hide:

    cp {{ np_versions }}/work2/nobel_prize.md .

.. prizerun::

    git status

We add the file to the staging area with ``git add``:

.. prizerun::

    git add nobel_prize.md

Now ``git status`` records this file being in the staging area, by listing it
under "changes to be committed":

.. prizerun::

    git status

Finally we move the changes from the staging area into a commit with ``git
commit``:

.. prizecommit:: commit_2_sha 2012-04-02 18:03.13

    git commit -m "Add first draft of paper"

Notice that the position of the current ``master`` branch is now this last
commit:

.. prizerun::

    git branch -v

.. prizerun::

    cat .git/refs/heads/master

We use ``git log`` to look at our short history.

.. prizerun::

    git log

We add the ``--parents`` flag to show that the second commit points back to
the first via its hash.  Git lists the parent hash after the commit hash:

.. prizerun::

    git log --parents

git diff |--| what has changed?
===============================

Our next commit has edits to the ``clever_analysis.py`` script.  We will also
refresh the figure from running the script.

I open the ``clever_analysis.py`` file in text editor and adjust the fudge
factor, add a new fudge factor, and apply the new factor to the data.

.. prizerun::
    :hide:

    # Copy the updated version from the local archive
    cp {{ np_versions }}/work3/clever_analysis.py .

Now I've done these edits, I can ask ``git diff`` to show me how the files in
my working tree differ from the files in the staging area.

Remember, the staging area refers to a snapshot as of the last commit.

.. prizerun::

    git diff

A ``-`` at the beginning of the ``git diff`` output means I have removed this
line.  A ``+`` at the beginning means I have added this line.  As you see I
have edited one line in this file, and added three more.

Open your text editor and edit ``clever_analysis.py``.  See if you can
replicate my changes by editing the file, and checking with ``git diff``.

Now check the status of ``clever_analysis.py`` with:

.. prizerun::

    git status

You need to ``git add`` a file to put it into the staging area
==============================================================

Remember that git only commits stuff that you have added to the staging area.

``git status`` tells us that ``clever_analysis.py`` has been "modified", and
that these changes are "not staged for commit".

There is a version of ``clever_analysis.py`` in the staging area, but it is
the version of the file as of the last commit, and so is different from the
version we have in the working tree.

If we try to do a commit, git will tell us there is nothing to commit, because
there is nothing new in the staging area:

.. prizerun::
    :allow-fail:

    git commit

To stage this version of ``clever_analysis.py`` to go into the next commit, we
use ``git add``:

.. prizerun::

    git add clever_analysis.py

Git status now shows these changes as "Changes to be committed".

.. prizerun::

    git status

Now we can update the figure by running ``analysis_script.py``.  The analysis
analyzes the data and writes the figure to the current directory.  If you have
Python installed, along with the ``numpy`` and ``matplotlib`` packages for
Python, you can run the analysis yourself with::

    python clever_analysis.py

If not, you can download a :download:`version of the figure I generated
earlier </np-versions/work3/fancy_figure.png>`.  After you have generated or
downloaded the figure:

.. prizerun::
    :hide:

    cp {{ np-versions }}/work3/fancy_figure.png .

.. prizerun::

    git add fancy_figure.png

Do a final check with ``git status``, then make the commit with:

.. prizecommit:: commit_3_sha 2012-04-03 11:20:01

    git commit -m "Add another fudge factor"

The branch bookmark has moved again:

.. prizerun::

    git branch -v

An ordinary day in gitworld
===========================

We now have the main commands for daily work with git;

* Make some changes in the working tree;
* Check what has changed with ``git status``;
* Review the changes with ``git diff``;
* Add changes to the staging area with ``git add``;
* Make the commit with ``git commit``.

Commit four
===========

For our next commit, we will add some more changes to the analysis script and
figure, and add a new file, ``references.bib``.

To follow along, first download :download:`references.bib
</np-versions/work4/references.bib>`.

.. prizerun::
    :hide:

    cp {{ np_versions }}/work4/references.bib .

Next, edit ``clever_analysis.py`` again, to make these changes:

.. prizerun::

    cp {{ np_versions }}/work4/clever_analysis.py .

.. prizerun::

    git diff

Finally regenerate ``fancy_figure.png``, or download the updated copy
:download:`from here </np-versions/work4/fancy_figure.png>`.

.. prizerun::

    cp {{ np_versions }}/work4/fancy_figure.png .

What will git status show now?

.. prizerun::

    git status

Git has not previously seen a file called ``refererences.bib`` so this file is
as yet "untracked".  Git has seen ``clever_analysis.py`` and
``fancy_figure.png``, so these files are tracked, and git sees that they are
modified compared to the copy that the staging area knows about.

Before we add our changes we confirm that they are as we expect with:

.. prizerun::

    git diff

Notice that git does not try and show the line-by-line differences between the
old and new figures, guessing correctly that this is a binary and not a text
file.

Now we have reviewed the changes, we add them to the staging area and commit:

.. prizerun::

    git add references.bib
    git add clever_analysis.py
    git add fancy_figure.png

.. prizecommit:: commit_4_sha 2012-04-04 01:40:42

    git commit -m "Change analysis and add references"

The branch bookmark has moved to point to the new commit:

.. prizerun::

    git branch -v

Undoing a commit with ``git reset``
===================================

As you found in the SAP story, this last commit doesn't look quite right,
because the commit message refers to two different types of changes.  With
more git experience, you will likely find that you like to break your changes
into commits where the changes have a particular theme or purpose.  This makes
it easier to see what happened when you look over the history and the commit
messages with ``git log``.

So, as in the SAP story, you decide to undo the last commit, and replace it
with two commits:

* One commit to add the changes to the script and figure;
* Another commit on top of the first.

In the SAP story, we had to delete a snapshot directory manually, and reset
the staging area directory to have the contents of the previous commit.  In
git, all we have to do is reset the current ``master`` branch bookmark to
point to the previous commit.  By default, git will also reset the staging
area for us.  The command to move the branch bookmark is ``git reset``.

Pointing backwards in history
=============================

The commit that we want the branch to point to is the previous commit in our
commit history.  We can use ``git log`` to see that this commit has hash
|commit_3_sha_7|.  So, we could do our reset with ``git reset``
|commit_3_sha_7|.  There is a simpler and more readable way to write this
common idea, of one commit back in history, and that is to add ``~1`` to a
reference.  For example, to refer to the commit that is one step back in the
history from the commit pointed to by the ``master`` branch, you can write
``master~1``.  Because ``master`` points to commit |commit_4_sha_7|, you could
also append the ``~1`` to |commit_4_sha_7|.  You can imagine that ``master~2``
will point two steps back in the commit history, and so on.

So, a readable reset command for our purpose is:

.. prizerun::

    git reset master~1

Notice that the branch pointer now points to the previous commit:

.. prizerun::

    git branch -v

Notice also that ``git reset`` has reset the staging area to the state as of
the given commit, but it has left the working tree alone.  That means that
``git status`` will show us the changes in the working tree compared to the
commit we have just reset to:

.. prizerun::

    git status

This kind of reset is called a "mixed" reset.  A "mixed" reset sets the branch
pointer, and sets the staging area to correspond to the current branch
pointer.  Try ``git reset --help`` for more detail.

Now we have the changes from our original fourth commit in our working tree,
but we have not staged them.  We are ready to make our new separate commits.

A new fourth commit
===================

As we planned, now we make a commit by adding only the changes from the script
and figure:

.. prizerun::

    git add clever_analysis.py
    git add fancy_figure.png

.. prizecommit:: commit_4_dash_sha 2012-04-04 1:40:42

    git commit -m "Change parameters of analysis"

Notice that git status now tells us that we still have untracked (and
therefore not staged) changes in our working tree:

.. prizerun::

    git status

Adding with ``-a``
==================

So far we have done our commits with at least two steps: ``git add`` and then
``git commit``.  It also possible to add files and commit the snapshot in one
step, using ``git commit -a``.

Adding the ``-a`` flag to ``git commit`` means that git will:

* ``add`` any modified, tracked files to the staging area;
* ``commit`` these modified files.

For example, I could have used ``git commit -a`` to combine the ``add`` and
``commit`` steps in the last commit.

Now we know how to undo a commit, let's undo the last commit and do it again
using ``git commit -a``.

.. prizerun::

    # Undo the last commit, reset staging area
    git reset master~1

As before, the working tree changes to script, figure and references now
differ from the copies known to the staging area:

.. prizerun::

    git status

Now I repeat the last commit, by adding the tracked files and doing the commit
in one step:

.. prizecommit:: commit_4_a_sha 2012-04-04 1:40:43

    git commit -a -m "Change parameters of analysis"

The ``-a`` flag to ``git commit`` ignores any untracked files |--| so
``references.bib`` will still be untracked:

.. prizerun::

    git status

.. note::

    If you have used other version control systems, the ``-a`` flag may look
    like a good idea, but experienced users often prefer to separate
    the add and commit steps using ``git add`` and ``git commit`` instead of
    ``git commit -a``.  We find the explicit ``git add`` helps us think about
    the changes we are adding, whereas the ``-a`` flag makes it easier to add
    changes we didn't intend.  So I recommend you always use ``git add``,
    especially when you are learning, and that's how I'm going to do the rest
    of the examples in this tutorial.

The fifth commit
================

To finish our work splitting the fourth commit into two, we add and commit the
``references.bib`` file:

.. prizerun::

    git add references.bib

.. prizecommit:: commit_5_sha 2012-04-04 2:10:02

    git commit -m "Add references"

Getting a file from a previous commit |--| ``git checkout``
===========================================================

In the SAP story, we found that the first version of the analysis script was
correct, and we made a new commit after restoring this version from the first
snapshot.

As you can imagine, git allows us to do that too.  The command to do this is
``git checkout``

If you have a look at ``git checkout --help`` you will see that git checkout
has two roles, described in the help as "Checkout a branch or paths to the
working tree".  We will see checking out a branch later, but here we are using
checkout in its second role, to restore files to the working tree.

We do this by telling git checkout which version we want, and what file we
want.  We want the version of ``clever_analysis.py`` as of the first commit.
To find the first commit, we can use git log.  To make git log a bit less
verbose, I've added the ``--oneline`` flag, to print out one line per commit:

.. prizerun::

    git log --oneline

Now we have the abbreviated commit hash for the first commit, we can checkout
that version to the working tree:

.. prizerun::

    git checkout {{ commit_1_sha_7 }} clever_analysis.py

We also want the previous version of the figure:

.. prizerun::

    git checkout {{ commit_1_sha_7 }} fancy_figure.png

Notice that the checkout also added the files to the staging area:

.. prizerun::

    git status

We are ready for our sixth commit:

.. prizecommit:: commit_6_sha 2012-04-05 18:40:04

    git commit -m "Revert to first version of script and figure"

Using bookmarks |--| ``git branch``
===================================

We are at the stage in the SAP story where Josephine goes away to the
conference.

Let us pretend that we are Josephine, and that we have taken a copy of the
working directory to the conference.

We as Josephine don't want to change your bookmark, which is ``master``:

.. prizerun::

    git branch -v

We would like to use our own bookmark, so we can make changes without
affecting anyone else.

::

    Git updates the current branch with the latest commit
    =====================================================

    Remember branches (bookmarks)?  Git has now moved the "master" branch location
    up to the new commit:

    .. prizerun::

        git log

    .. prizerun::

        git branch -v

    .. prizerun::

        cat .git/refs/heads/master

    Our most recent commit (|a-flag|) has the previous commit (|fruit|) as a
    parent.  |fruit| has |initial| as a parent.  |initial| is the first commit,
    and has no parent:

    .. prizerun::

        git log --parents

    A nicer log command using ``git config``
    ========================================

    It is very often useful to see a summarized version of the log.  Here is a
    useful set of command flags for git log:

    .. prizerun::

        git log --oneline --topo-order --graph

    Git supports *aliases:* new names given to command combinations. Let's
    make this handy shortlog an alias, so we only have to type ``git slog``
    to get this compact log.

    We create our alias (this saves it in git's permanent configuration file):

    .. prizerun::

        git config --global alias.slog "log --oneline --topo-order --graph"

    And now we can use it:

    .. prizerun::

        git slog

    .. _git-tag:

    git tag makes a static bookmark
    ===============================

    We have seen that a branch is a bookmark that points to a commit.

    When we do a new commit on a branch, the branch points to the new commit.

    We can also make bookmarks that do not update when we do a commit.  These are
    git *tags*.

    Imagine we are now happy with the state of our paper, and we submit it to
    Science.

    We want to record the exact state of the paper when we sent it to Science,
    because we may need to go back to this version when those nasty Science
    reviewers ask us to make changes.

    We could write down the current commit hash somewhere, but then we might lose
    it.  Luckily ``git tag`` has a better solution:

    .. prizerun::

        git tag submitted-to-science

    We now have a tag with name ``submitted-to-science`` that points to this
    commit.  As we will see, unlike a branch, the tag does not change when you do
    another commit.

    The current commit is:

    .. prizerun::

        git branch -v

    ``git tag`` without arguments will list the current tags:

    .. prizerun::

        git tag

    As you can imagine, this tag is very similar to a branch |--| it is just a
    tiny file where the name of the file is the tag name, and the contents is the
    commit hash:

    .. prizerun::

        ls .git/refs/tags

    .. prizerun::

        cat .git/refs/tags/submitted-to-science

    This type of tag is what git calls a *lightweight* tag |--| it is just a
    bookmark to a commit, with no other information.

    We often want to add some extra information to our tags, such as a message
    about what the tag is for, the date, and the person doing the tag.  We can do
    this with *annotated tags*. To make an annotated tag, use the ``-a`` flag to
    ``git tag`` and give a tag message:

    .. prizecommit:: dummy-label 2012-04-01 12:13:34

        git tag -a -m "Submitted to Science" annotated-to-science

    .. note::

        I'm using the the ``-m`` flag as I have for the commits, and for the same
        reason.  Normally you would not use ``-m`` and let the text editor open
        for you to type the tag message.

    .. prizerun::

        git tag

    There is still a tiny text file for the tag:

    .. prizerun::

        ls .git/refs/tags

    This time the tag does not point to a commit hash, but to a new tag object:

    .. prizerun::

        cat .git/refs/tags/annotated-to-science

    .. prizevar:: annotated-to-science

        cat .git/refs/tags/annotated-to-science

    The new tag object is very much like a commit object, but pointing to a commit
    object rather than a tree object:

    .. prizerun::

        git cat-file -p {{ annotated-to-science }}

    Unlike a branch, a tag does not change when we make a commit:

    .. prizerun::

        git branch -v

    .. prizecommit:: after-science 2012-04-01 12:13:01

        echo "Actually, maybe this is all wrong" >> nobel_prize_paper.txt
        git add nobel_prize_paper.txt
        git commit -a -m "Luckily we submitted the paper before we realized"

    The branch bookmark has changed:

    .. prizerun::

        git branch -v

    But the tags have not changed:

    .. prizerun::

        cat .git/refs/tags/submitted-to-science

    .. prizerun::

        cat .git/refs/tags/annotated-to-science

    You have now seen all the possible types of objects in ``.git/objects``.  See
    :ref:`git-object-types` for a review.

    git mv and rm: moving and removing files
    ========================================

    While ``git add`` is used to add files to the list of files that git tracks,
    we must also tell it if we want their names to change or for it to stop
    tracking them. In familiar Unix fashion, the ``mv`` and ``rm`` git commands do
    precisely this:

    .. prizerun::

        git mv very_clever_analysis.py slightly_dodgy_analysis.py
        git status

    Note that these changes must be committed too, if we want to keep them.

    .. prizecommit:: new-name 2012-04-01 13:15:01

        git commit -m "I like this new name better"

    As you can imagine, all that changed is that the tree object for this commit
    associates the new filename with the old hash for the file.  I will use the
    obscure ``git ls-tree`` command as a shortcut to show me the contents of the
    root tree object for this commit:

    .. prizerun::

        git ls-tree master

    ``git rm`` works in a similar fashion.

    git branch again - making a new branch
    ======================================

    Remember that a branch is simply a bookmark pointing to a particular commit.

    We can have multiple branches in a repository, where each one may point to a
    different commit.

    At the moment, we only have one branch, "master":

    .. prizerun::

        git branch -v

    We can make a new branch with the ``git branch`` command:

    .. prizerun::

        git branch experiment
        git branch -v

    The new branch, by default, points to the commit we are currently on, and this
    commit is the also the commit that the "master" branch points to.  So, at the
    moment "master" and "experiment" point to the same commit.

    Of course this new branch is also just a tiny text file with the name of the
    branch and the commit that it currently points to:

    .. prizerun::

        ls .git/refs/heads

    .. prizerun::

        cat .git/refs/heads/experiment

    git ``HEAD`` points to the current branch
    =========================================

    Remember that, when you make a new commit, git moves the branch pointer to
    point at the new commit.  Now we have two branches, how does git know which is
    the current branch, in order to move the right branch pointer when you make a
    commit?

    This information goes in a special git pointer, called ``HEAD``.  HEAD stores
    the name of the current branch. HEAD is just a tiny text file storing the
    current branch:

    .. prizerun::

        cat .git/HEAD

    Here, HEAD is pointing to the "master" branch.  The master branch is pointing
    to a particular commit:

    .. prizerun::

        git branch -v

    Heads and refs
    ==============

    For git, a *reference* or a *ref* is a name that refers to another object. A
    reference almost invariably points to a commit object [#tag-other-objects]_.

    For example a branch is a reference, and so is a tag. Remember that git stores
    branches and tags in ``.git/refs``.

    A *head* is a reference to a commit that updates when we do ``git commit``.
    All branches are heads.  A tag is not a head because it does not update when
    we do a commit.  Remember that git stores branches in ``.git/refs/heads``.
    The special reference HEAD points to the current head that we are working on.

    Developing on different branches
    ================================

    Let's now illustrate all of this with a concrete example. We get our bearings
    first:

    .. prizerun::

        git status

    .. prizerun::

        ls

    We are now going to try two different routes of development: we will add one
    file on on the ``experiment`` branch, and we will add another file on the
    ``master`` branch. We will then merge the ``experiment`` branch into
    ``master``.

    How do we start working on this branch ``experiment`` rather than
    ``master``?

    git checkout - set the current branch, set the working tree from a commit
    =========================================================================

    Up until now we have been on the ``master`` branch. When we make a
    commit, the ``master`` branch pointer (``.git/refs/heads/master``) moves
    up to point to our most recent commit.

    ``git checkout`` can switch us to using another branch:

    .. prizerun::

        git checkout experiment

    What just happened?

    The current branch has changed (notice the asterisk in front of
    ``experiment``).

    .. prizerun::

        git branch -v

    Git ``HEAD`` now points to the ``experiment`` branch:

    .. prizerun::

        cat .git/HEAD

    As we'll see later, ``git checkout somebranch`` also sets the contents
    of the working tree to match the commit contents for ``somebranch``. In
    this case the commits for ``master`` and ``experiment`` are currently
    the same, meaning they have the same corresponding working tree, so our
    working tree did not change.

    Now let's do some changes on the ``experiment`` branch:

    .. prizecommit:: an-experiment 2012-04-01 13:13:13

        echo "Some crazy idea" > an_experiment.txt
        git add an_experiment.txt
        git commit -m "Trying something new"

    .. prizerun::

        git slog

    Notice we have a new file called ``an_experiment.txt`` in this branch:

    .. prizerun::

        ls

    The ``experiment`` branch pointer has now moved up to the current commit:

    .. prizerun::

        cat .git/refs/heads/experiment

    But the ``master`` branch points to the same place as it did before:

    .. prizerun::

        git branch -v

    git checkout again - get a new working tree
    ===========================================

    If ``somewhere`` is a branch name, then ``git checkout somewhere``
    selects ``somewhere`` as the current branch. It also resets the working
    tree to match the working tree for that commit.

    .. prizerun::

        git checkout master

    .. prizerun::

        cat .git/HEAD

    We're back to the working tree as of the ``master`` branch;
    ``an_experiment.txt`` has gone now.

    .. prizerun::

        ls

    Meanwhile we do some more work on master:

    .. prizerun::

        git slog

    .. prizecommit:: boring 2012-04-01 13:43:13

        echo "All the while, more work goes on in master..." >> boring_idea.txt
        git add boring_idea.txt
        git commit -m "The mainline keeps moving"

    .. prizerun::

        git slog

    git merge - merging changes from different branches
    ===================================================

    We do a merge when we have made some changes in one branch, and we want to
    bring (merge) these changes into another branch.

    The typical situation is where we have made some useful changes in an
    experimental branch - like our ``experiment`` branch, and we decide we want to
    make these changes part of the main line of development - often the ``master``
    branch.

    Here is the merge:

    .. prizecommit:: merge-experiment 2012-04-01 14:01:10

        git merge experiment -m "Merge in the experiment"

    Notice now that the master branch has the new file ``an_experiment.txt`` from
    the ``experiment`` branch, as well as the new file ``boring_idea.txt`` from
    the master branch:

    .. prizerun::

        ls

    The git log output shows us two lines of development diverging and then
    merging:

    .. prizerun::

        git slog

    The merge commit has two "parent" commits, which are the previous commit on
    ``master`` and the previous commit on ``experiment``:

    .. prizerun::

        git slog --parents

    An important aside: conflict management
    =======================================

    While git is very good at merging, if two different branches modify the
    same file in the same location, it simply can't decide which change
    should prevail. At that point, human intervention is necessary to make
    the decision. Git will help you by marking the location in the file that
    has a problem, but it's up to you to resolve the conflict. Let's see how
    that works by intentionally creating a conflict.

    We start by making another new branch and making a change to our experiment
    file:

    .. prizerun::

        git branch trouble
        git checkout trouble

    .. prizecommit:: trouble-starts 2012-04-01 14:23:13

        echo "This is going to be a problem..." >> an_experiment.txt
        git add an_experiment.txt
        git commit -m "Changes in the trouble branch"

    And now we go back to the master branch, where we change the *same*
    file:

    .. prizecommit:: while-trouble 2012-04-01 14:29:13

        git checkout master
        echo "More work on the master branch..." >> an_experiment.txt
        git add an_experiment.txt
        git commit -m "Mainline work"

    So now let's see what happens if we try to merge the ``trouble`` branch
    into ``master``:

    .. prizerun::

        git merge trouble -m "Unlikely this one will work"

    Let's see what git has put into our file:

    .. prizerun::

        cat an_experiment.txt

    The text between ``<<``... and ``==``... gives the changes added by our
    current branch |--| ``HEAD``.  These are the changes introduced by the branch
    we are merging *into*.

    The text between ``==``... and ``>>``... gives the changes added by the
    ``trouble`` branch.  These are the changes introduced by the branch we are
    merging *from*.

    At this point, we can go into the file with a text editor, decide which
    changes to keep, and make a new commit that records our decision.

    I decided that both pieces of text were useful, but I want to integrate them
    with some changes.  I do the edits by writing the file I want directly:

    .. prizewrite::

        # file: an_experiment.txt
        Some crazy idea
        More work on the master branch...
        This is no longer going to be a problem...

    .. prizerun::

        git status

    Let's then make our new commit:

    .. prizecommit:: merge-trouble 2012-04-01 14:33:13

        git add an_experiment.txt
        git commit -m "Completed merge of trouble, fixing conflicts along the way"

    .. prizerun::

        git slog

    .. _git-graph:

    Git commits form a graph
    ========================

    The output of ``git slog`` shows the sequence of commits as a graph.

    The nodes of the graph are the commits. Each commit has one or more parents,
    stored in the commit object.  The parents give the links between the commit
    and the previous commit(s) in the *commit history* graph.  The commit parents
    therefore give links that form the edges in the graph.

    git remotes - working with other people, making backups
    =======================================================

    Now you are keeping the history of your data, you also want to make sure you
    have a backup in case your laptop dies.

    You might want to work with a friend on the same project.  Perhaps your friend
    Anne is also working on the paper, and you want to merge her changes into
    yours.

    We use git "remotes" to solve both of these problems.

    Keeping backups with remotes
    ============================

    Let's say you have an external backup disk and you want to record all the
    history of your work on the backup disk.

    To do this you need three steps:

    * Make an empty backup repository on the external backup disk
    * Point your current git repository at the backup repository with ``git remote
    add``
    * Send the changes to the backup repository with ``git push``

    Make the empty backup repository
    --------------------------------

    .. workvar:: usb_mountpoint
        :var_type: render

        echo "/Volumes/my_usb_disk"

    .. workvar:: usb_mountpoint
        :var_type: run
        :omit_link:

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
    files in the |usb_mountpoint| backup
    repository, we will only be editing files in our local ``nobel_prize``
    directory, committing those changes locally (as we have done above), and then
    "pushing" these changes to the backup repository [#bare-detail]_.

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

        tree -a {{ usb_mountpoint }}/nobel_prize.git/objects

    Then we push:

    .. prizerun::

        git push usb_backup master

    This command tells git to take all the information necessary to reconstruct
    the history of the ``master`` branch, and send it to the remote repository.
    Sure enough, we now have files in ``.git/objects`` of the backup repository:

    .. desktoprun::

        tree -a {{ usb_mountpoint }}/nobel_prize.git/objects

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

    First we make a new commit in the local repository:

    .. prizecommit:: buffing 2012-04-01 15:13:13

        echo "Express confidence in the study" >> nobel_prize_paper.txt
        git add nobel_prize_paper.txt
        git commit -m "Buff up the paper some more"

    Git updated the local ``master`` branch, but the remote does not know about
    this update yet:

    .. prizerun::

        git branch -a -v

    We already know there will be three new objects in ``.git/objects`` after this
    commit.  These are:

    * a new blob (file) object for the modified ``nobel_prize_paper.txt``;
    * a new tree (directory listing) object associating the new hash for the
    contents of ``nobel_prize_paper.txt`` with the ``nobel_prize_paper.txt``
    filename;
    * the new commit object.

    Usually we don't need to worry about which objects these are, but here we will
    track these down to show how ``git push`` works.

    The commit object we can see from the top of ``git log``. The ``-1`` flag to
    ``git log`` tells git to show just the most recent commit from the log:

    .. prizerun::

        git log -1

    So the commit is |buffing|. We can get the tree object from the commit object:

    .. prizerun::

        git cat-file -p {{ buffing }}

    We can show the tree object contents to get the object for the new
    version of ``nobel_prize_paper.txt``.

    .. depends on history

    .. prizevar:: buffing-fname

        commit={{ buffing }}
        echo ${commit:0:2}/${commit:2}

    .. prizevar:: buffing-tree

        git log -1 --format="%T"

    .. prizevar:: buffing-tree-fname

        tree={{ buffing-tree }}
        echo ${tree:0:2}/${tree:2}

    .. prizerun::

        git cat-file -p {{ buffing-tree }}

    .. prizevar:: buffing-paper-obj

        git cat-file -p {{ buffing-tree }} | grep nobel_prize | awk '{print $3}'

    .. prizevar:: buffing-paper-obj-fname

        obj={{ buffing-paper-obj }}
        echo ${obj:0:2}/${obj:2}

    We do have these objects in the local repository:

    .. prizerun::

        ls .git/objects/{{ buffing-fname }}
        ls .git/objects/{{ buffing-tree-fname }}
        ls .git/objects/{{ buffing-paper-obj-fname }}

    |--| but we don't have these objects in the remote repository yet (we haven't
    done a ``push``):

    .. prizerun::

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

    Now we want a repository with a working tree.

    .. workrun::
        :hide:

        mkdir repos

    The command we want is ``git clone``:

    .. laptoprun::

        git clone {{ usb_mountpoint }}/nobel_prize.git

    We have a full backup of the repository, including all the history:

    .. laptoprun::

        cd nobel_prize
        git slog

    git made a ``remote`` automatically for us, because it recorded where we
    cloned from.  The default name for a git remote is ``origin``:

    .. prizelaprun::

        git remote -v

    Of course, just after the clone, the remote and the local copy are
    synchronized:

    .. prizelaprun::

        git branch -a -v

    Now we could make some commits.

    .. prizelapcommit:: wine-ideas 2012-04-01 20:13:31

        echo "The brain is a really big network." >> nobel_prize_paper.txt
        git add nobel_prize_paper.txt
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
    * ``git pull`` (this is just a ``git fetch`` followed by a ``git merge``).

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
    because it just involves advancing the branch pointer, rather than fusing two
    lines of development:

    .. prizerun::

        git slog

    git pull |--| git fetch followed by git merge
    ---------------------------------------------

    ``git pull`` is just a shortcut for ``git fetch`` followed by ``git merge``.

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

    We do a commit:

    .. prizecommit:: no-network 2012-04-02 11:13:13

        echo "Is the network comment too obvious?" >> nobel_prize_paper.txt
        git add nobel_prize_paper.txt
        git commit -m "Rethinking the drinking again"

    Now instead of ``git push usb_backup master`` we can just do ``git push``.

    Before we try this, we need to set a default configuration variable to avoid a
    confusing warning. See ``git config --help`` for more detail:

    .. prizerun::

        git config push.default simple

    .. prizerun::

        git push

    Git also knows what to do if we do ``git fetch`` from this branch.

    To show this at work, we go home to the laptop, fetch the desktop work from
    the USB drive, and then do another commit from the laptop:

    .. laptoprun::

        cd nobel_prize
        git fetch origin
        git merge origin/master

    .. prizelapcommit:: convinced 2012-04-02 22:13:31

        echo "More convinced by networks." >> nobel_prize_paper.txt
        git add nobel_prize_paper.txt
        git commit -m "I think better at home"

    Then push back to the USB disk, setting the link between the laptop branch and
    the remote for good measure:

    .. prizelaprun::

        git push origin master --set-upstream

    Back to the work desktop to demonstrate "fetch" after we have done ``git
    push`` with ``--set-upstream`` above:

    .. prizerun::

        git fetch

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

    Other useful commands
    =====================

    These commands complete the typical daily toolkit of an experienced git user:

    *  `reflog <http://www.kernel.org/pub/software/scm/git/docs/git-reflog.html>`__
    *  `rebase <http://www.kernel.org/pub/software/scm/git/docs/git-rebase.html>`__

    See :doc:`rebase_without_tears` for a tutorial on ``rebase``.

    Git: are you ready?
    ===================

    If you followed this tutorial, you now have a good knowledge of how git works.
    This will make it much easier to understand why git commands do what they do,
    and what to do when things go wrong.  You know all the main terms that the git
    manual pages use, so git's own help will be more useful to you.  You will
    likely lead a long life of deep personal fulfillment.

*************
Git resources
*************

Introductions and tutorials
===========================

As you've seen, this tutorial makes the bold assumption that you'll be able to
understand how git works by seeing how it is *built*. These documents take a
similar approach to varying levels of detail:

* This `visual git tutorial
  <http://www.ralfebert.de/blog/tools/visual_git_tutorial_1>`__ gives a nice
  visual idea of git at work.
* `Understanding Git Conceptually
  <http://www.sbf5.com/~cduan/technical/git>`__ gives another review of how
  the ideas behind git.
* For more detail, see the start of the excellent `Pro Git
  <http://progit.org/book>`__ online book, or similarly the early parts of the
  `Git community book <http://book.git-scm.com>`__. Pro Git's chapters are
  very short and well illustrated; the community book tends to have more
  detail and has nice screencasts at the end of some sections.
* The `Git parable
  <http://tom.preston-werner.com/2009/05/19/the-git-parable.html>`__ by Tom
  Preston-Werner.
*  :doc:`foundation`

You might also try:

* For windows users, `an Illustrated Guide to Git on Windows
  <http://nathanj.github.com/gitguide/tour.html>`__ is useful in that it
  contains also some information about handling SSH (necessary to interface
  with git hosted on remote servers when collaborating) as well as screenshots
  of the Windows interface.
* `Git ready <http://www.gitready.com>`__ A great website of posts on specific
  git-related topics, organized by difficulty.
* `QGit <http://sourceforge.net/projects/qgit/>`__: an excellent Git GUI Git
  ships by default with gitk and git-gui, a pair of Tk graphical clients to
  browse a repo and to operate in it. I personally have found `qgit
  <http://sourceforge.net/projects/qgit/>`__ to be nicer and easier to use. It
  is available on modern Linux distros, and since it is based on Qt, it should
  run on OSX and Windows.
* `Git Magic
  <http://www-cs-students.stanford.edu/~blynn/gitmagic/index.html>`_ : Another
  book-size guide that has useful snippets.
* The `learning center <http://learn.github.com>`__ at Github Guides on a
  number of topics, some specific to github hosting but much of it of general
  value.
* A `port <http://cworth.org/hgbook-git/tour>`__ of the Hg book's beginning
  The `Mercurial book <http://hgbook.red-bean.com>`__ has a reputation for
  clarity, so Carl Worth decided to `port
  <http://cworth.org/hgbook-git/tour>`__ its introductory chapter to Git. It's
  a nicely written intro, which is possible in good measure because of how
  similar the underlying models of Hg and Git ultimately are.
* `Intermediate tips
  <http://andyjeffries.co.uk/articles/25-tips-for-intermediate-git-users>`_: A
  set of tips that contains some very valuable nuggets, once you're past the
  basics.

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

* `git-completion.bash
  <https://github.com/git/git/blob/master/contrib/completion/git-completion.bash>`__
* `git-prompt.sh
  <https://github.com/git/git/blob/master/contrib/completion/git-prompt.sh>`__

You can then source both of these files in your ``~/.bashrc`` (Linux) or
``~/.bash_profile`` (OSX), and then set your prompt (I'll assume you
named them as the originals but starting with a ``.`` at the front of
the name):

::

    source $HOME/.git-completion.bash
    source $HOME/.git-prompt.sh
    PS1='[\u@\h \W$(__git_ps1 " (%s)")]\$ ' # adjust this to your prompt liking

See the comments in both of those files for lots of extra functionality
they offer.

.. rubric:: Footnotes

.. [#tree-command] I am using the ``tree`` command to give a nice text-graphic
   listing of directories.  If you want to try running ``tree`` yourself, you
   may need to find an implementation of ``tree`` for your operating system.
   On Debian or Ubuntu you can use ``sudo apt-get install tree``. For OSX you
   might want to use something like homebrew (``brew install tree``).  I have
   not tried installing ``tree`` on Windows.
.. [#list-figure] Would I get the same hash for the directory listing if I had
   had a different figure?  No |--| because the figure hash would be
   different, the directory listing would contain this different hash, and so
   the hash for the directory listing must be different.
.. [#commit-figure] Would the commit hash value change if the figure changed?
   Yes, because the change in the figure would cause a different hash for the
   figure; this would cause a different hash for the directory listing, and
   this hash in turn appears in the commit contents, causing a different hash
   for the commit.
.. [#no-parents] Why are the output of ``git log`` and ``git log --parents``
   the same in this case?  They are the same because this is the first commit,
   and the first commit has no parents.
.. [#git-object-dir] When git stores a file in the ``.git/objects`` directory,
   it makes a hash from the file, takes the first two digits of the hash to
   make a directory name, and then stores a file in this directory with a
   filename from the remaining hash digits.  For example, when adding a file
   with hash ``d92d079af6a7f276cc8d63dcf2549c03e7deb553`` git will create
   ``.git/objects/d9`` directory if it doesn't exist, and stores the file
   contents as ``.git/objects/d9/2d079af6a7f276cc8d63dcf2549c03e7deb553``.  It
   does this so that the number of files in any one directory stay in a
   reasonable range.  If git had to store hash filenames for every object in
   one flat directory, the directory would soon have a very large number of
   files.
.. [#tag-other-objects] You might have guessed by now that a tag can refer to
   any git object, not just a commit.  For example a tag can refer to a tree
   (directory listing) or blob (file) object, although in practice tags almost
   always refer to commits.
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
