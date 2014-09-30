.. _git-object-types:

####################
Types of git objects
####################

If you have read :doc:`curious_git`, you know all the different types of
objects that git stores in ``.git/objects``.  The object types are:

* *blob*;
* *tree*;
* *commit*;
* *tag*.

Here we use examples from one particular commit in the ``nobel_prize``
repository from :doc:`curious_git`.

The commit is the commit we tagged as ``submitted-to-science``.  The hash for
the commit is:

.. prizerun::

    cat .git/refs/tags/submitted-to-science

Here is the working tree for the ``nobel_prize`` repository as of that commit:

.. prizerun::
    :hide:

    git checkout {{ a-flag }}

.. prizerun::

    ls

Blob object type
----------------

*Blob* is an abbreviation for "binary large object".  When we ``git add`` a
file such as ``nobel_prize_paper.txt``, git creates a *blob* object containing
the contents of the file.  Blobs are therefore the git object type for storing
files.

The ``git rev-parse`` command will give me the hash value for individual
objects.  ``git cat-file -t`` will show us the type of a git object given a
hash. ``git cat-file -p`` shows us the content of the object.

.. note::

    ``git rev-parse`` and ``git cat-file`` are obscure git commands and it is
    quite possible you will never need to use them in your daily git work.
    I'm using them here to show how the git machinery works.  Feel free to
    forget about them after you've read this page.

Here is the object hash value for the ``nobel_prize_paper.txt`` file as of our
example commit:

.. prizerun::

    git rev-parse {{ a-flag }}:nobel_prize_paper.txt

.. prizevar:: a-flag-paper-obj

    git rev-parse {{ a-flag }}:nobel_prize_paper.txt

The corresponding object is of type *blob*:

.. prizerun::

    git cat-file -t {{ a-flag-paper-obj }}

The contents of the blob are the contents of the paper as of this commit:

.. prizerun::

    git cat-file -p {{ a-flag-paper-obj }}

Tree object type
----------------

There is an object type for a directory listing, called a *tree* object.

Here is the tree object hash for the root directory listing as of this commit:

.. prizerun::

    git rev-parse {{ a-flag }}:./

.. prizevar:: a-flag-tree

    git rev-parse {{ a-flag }}:./

The object is of type "tree":

.. prizerun::

    git cat-file -t {{ a-flag-tree }}

The tree object contains one line per file or subdirectory, with each line
giving file permissions, *object type*, object hash and filename.  *Object
type* is usually one of "blob" for a file or "tree" for a subdirectory
[#directory-tree-types]_.

.. prizerun::

    git cat-file -p {{ a-flag-tree }}

Notice the line linking the hash value |a-flag-paper-obj| with the filename
``nobel_prize_paper.txt``.

Commit object type
------------------

We already know that the hash of the current commit object is |a-flag|.  This
is an object of type "commit":

.. prizerun::

    git cat-file -t {{ a-flag }}

The commit object contains the directory tree object hash, parent commit hash,
author, committer, date and message:

.. prizerun::

    git cat-file -p {{ a-flag }}

Notice the root tree hash is |a-flag-tree| as we were expecting.

Tag object type
---------------

There is also an annotated git *tag* object type.  We made one of these in the
:ref:`git-tag` section of :doc:`curious_git`.

.. prizerun::

    cat .git/refs/tags/annotated-to-science

The object is of type "tag":

.. prizerun::

    git cat-file -t {{ annotated-to-science }}

The tag object type contains the hash of the tagged object, the type of tagged
object (usually a commit), the tag name, author, date and message:

.. prizerun::

    git cat-file -p {{ annotated-to-science }}

Notice that the tagged object is the commit object |a-flag|, as we were
expecting.

.. rubric:: Footnotes

.. [#directory-tree-types] The object types in a directory listing are almost
   invariably either "blob" or "tree", but can also be "commit" for recording
   the commit of a git submodule - see :doc:`git_submodules`.

.. include:: links_names.inc
.. include:: working/object_names.inc

