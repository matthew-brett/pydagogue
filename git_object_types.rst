.. _git-object-types:

####################
Types of git objects
####################

If you have read :doc:`curious_git`, you know that git stores different types
of objects in ``.git/objects``.  The object types are:

* *commit*;
* *tree*;
* *blob*;
* *annotated tag*.

Here we make examples of each of these object types in a new repository.

First we make the working tree and initialize the repository:

.. workrun::
    :hide:

    rm -rf example_repo

.. workrun::

    mkdir example_repo
    cd example_repo
    git init

Next we make an example commit:

.. workrun::
    :cwd: /working/example_repo

    echo "An example file" > example_file.txt
    git add example_file.txt
    git commit -m "An example commit"

From :doc:`curious_git`, we expect there will now be three objects in the
directory ``.git/objects``, one storing the backup of ``example_file.txt``,
one storing the directory listing for the commit, and one storing the commit
message:

.. workout::

    ../tools/mytree.py example_repo/.git/objects

******************
Commit object type
******************

The commit object contains the directory tree object hash, parent commit hash,
author, committer, date and message.

Git log will show us the hash for the commit message:

.. workrun::
    :cwd: /working/example_repo

    git log

.. workvar:: eg_commit_hash

    cd example_repo
    git rev-parse HEAD

.. note::

    I'll use ``git cat-file`` to show the contents of the hashed files in
    ``.git/objects``, but ``cat-file`` is a relatively obscure git command
    that you will probably not need in your daily git work.

``git cat-file -t`` shows us the type of the object represented by a
particular hash:

.. workrun::
    :cwd: /working/example_repo

    git cat-file -t {{ eg_commit_hash }}

``git cat-file -p`` shows the contents of the file associated with this hash:

.. workrun::
    :cwd: /working/example_repo

    git cat-file -p {{ eg_commit_hash }}

****************
Tree object type
****************

The commit contents gave us the hash of the directory listing for the
commit.  If we inspect this object, we find it is of type "tree" and contains
the directory listing for the commit:

.. workvar:: eg_tree_hash

    cd example_repo
    git rev-parse HEAD:./

.. workrun::
    :cwd: /working/example_repo

    git cat-file -t {{ eg_tree_hash }}

.. workrun::
    :cwd: /working/example_repo

    git cat-file -p {{ eg_tree_hash }}

The tree object contains one line per file or subdirectory, with each line
giving file permissions, *object type*, object hash and filename.  *Object
type* is usually one of "blob" for a file or "tree" for a subdirectory
[#directory-tree-types]_.

****************
Blob object type
****************

The directory listing gave us the hash of the stored of ``example_file.txt``.
This object is of type "blob" and contains the file snapshot:

.. workvar:: eg_file_hash

    cd example_repo
    git rev-parse HEAD:example_file.txt

.. workrun::
    :cwd: /working/example_repo

    git cat-file -t {{ eg_file_hash }}

.. workrun::
    :cwd: /working/example_repo

    git cat-file -p {{ eg_file_hash }}

*Blob* is an abbreviation for "binary large object".  When we ``git add`` a
file such as ``example_file.txt``, git creates a *blob* object containing the
contents of the file.  Blobs are therefore the git object type for storing
files.

***************
Tag object type
***************

There is also a git type for annotated tags.  We don't have one of those yet,
so let's make one:

.. workrun::
    :cwd: /working/example_repo

    git tag -a first-commit -m "Tag pointing to first commit"

This gives us a new object in ``.git/objects``:

.. workout::

    ../tools/mytree.py example_repo/.git/objects

.. workvar:: eg_tag_hash

    cd example_repo
    git rev-parse first-commit

The object is of type "tag":

.. workrun::
    :cwd: /working/example_repo

    git cat-file -t {{ eg_tag_hash }}

The tag object type contains the hash of the tagged object, the type of tagged
object (usually a commit), the tag name, author, date and message:

.. workrun::
    :cwd: /working/example_repo

    git cat-file -p {{ eg_tag_hash }}

Notice that the "object" the tag points to, via its hash, is the commit
object, as we were expecting.

.. rubric:: Footnotes

.. [#directory-tree-types] The object types in a directory listing are almost
   invariably either "blob" or "tree", but can also be "commit" for recording
   the commit of a git submodule - see :doc:`git_submodules`.

.. include:: links_names.inc
.. include:: working/object_names.inc
