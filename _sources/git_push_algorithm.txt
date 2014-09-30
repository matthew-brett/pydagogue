#########################
An algorithm for git push
#########################

We saw how git stores its object in :doc:`curious_git`.

Now we know about how git stores its objects, we can work out how git knows
which objects to copy when it does a push.

Something like this algorithm might do the job:

#. Get the commit hash corresponding the branch we are going to push;
#. Follow every :ref:`commit path <git-graph>` back from this commit, until we hit a commit hash
   (filename) that the remote has.  All the previous commits on the path, that
   the remote does not have, are *missing commits*; #. For every *missing
   commit* get the corresponding tree (directory listing) object.  If the tree
   object is not in the remote objects directory, add to
   the list of *missing trees*;
#. For every *missing tree* read the tree directory listing. Find any blob
   (file) objects in the directory listing that are not in the remote objects
   directory, add to the list of *missing blob* objects [#sub-trees]_;
#. Copy all *missing commit*, *missing tree* and *missing blob* objects to the
   remote objects directory;
#. Update the remote branch to point to the same commit as the local branch;
#. Update the local record of the last known position of the remote branch to
   point to the same commit.

There's a specific example of ``git push`` at :ref:`git-push`. Here is how
that example would follow our algorithm:

#. We look up the hash for ``master``, and we get |buffing| (abbreviated as
   |buffing-7|);
#. We follow all commit history paths back from |buffing-7| to check for
   missing commits. We start with |buffing-7|. The remote does not have a
   matching file in ``objects``, so this is a missing commit. We only have one
   path to follow, because |buffing-7| has only one parent |--|
   |merge-trouble-7| |--| and the remote does have a corresponding object, so
   we can stop looking for missing commits;
#. We only have one missing commit, |buffing-7|.  We look in the contents of
   |buffing-7| to find the tree object hash.  This is |buffing-tree|.  We
   check for this object in the remote objects directory, and sure enough, it
   is missing. We add this tree to the list of missing trees;
#. We only have one missing tree |--| |buffing-tree|. We look in the contents
   of this tree object and check in the remote object directory for each
   object in this listing. The only missing object is |buffing-paper-obj|;
#. We copy the objects for the missing commits (|merge-trouble|), missing
   trees (|buffing-tree|) and missing blobs (|buffing-paper-obj|) to the
   remote objects directory;
#. We set remote ``refs/heads/master`` to contain the hash |buffing|;
#. Set the local ``refs/remotes/usb_backup/master`` to contain |buffing|.

.. rubric:: Footnotes

.. [#sub-trees] You have probably worked out by now that git directory
   listings can have files (called "blobs") and subdirectories ("trees").
   When doing the copy, we actually have to recurse into any sub-directories
   to get needed file ("blob") and subdirectory ("tree") objects.  But, you
   get the idea.

.. include:: links_names.inc
.. include:: working/object_names.inc
