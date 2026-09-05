---
jupytext:
  text_representation:
    extension: .md
    format_name: myst
    format_version: 0.13
    jupytext_version: 1.16.6
kernelspec:
  display_name: Bash
  language: bash
  name: bash
---

# Git-Annex from scratch

I found I missed an under-the-hood explanation of what Git-Annex added on top
of an ordinary Git repository.

I'm partly starting from [Joey Hess' talk](https://www.youtube.com/watch?v=zQTAeX4prZo).

Here is a set of fundamental objects for Git-Annex, from that talk:

## Git-Annex objects (GAOs)

GAOs are objects in the same sense that Git stores *objects* in its object
store.

For *Git* (not Git-Annex), when we do `git add myfile`, Git takes the contents
of `myfile` (well, in fact, a compressed version of `myfile`) and copies it
into the `.git/objects` directory, with a filename generated from the SHA1 hash
of the object.

However, Git-Annex is designed to work with very large files that should not be
compressed or copied.  So when you create a Git-Annex object (with `git annex
add mybigfile`):

* The file is *moved*, not copied.
* Within the working tree, Git-Annex leaves behind a pointer (usually
  a symbolic link) to the now-moved file.  See below.
* The moved file is not compressed.
* The contents go into `.git/annex/objects` instead of `.git/objects`.
* Git-Annex removes write permission on the moved file, to prevent you
  overwriting the file accidentally (see
  [lock](https://git-annex.branchable.com/git-annex-lock/)/[unlock](https://git-annex.branchable.com/git-annex-unlock/)).
* There are different rules for making the hash filename that we don't need to
  worry about for now.

## Git-Annex pointers

Above, we said that when we make a file into a Git-Annex object, we leave
a *pointer* to the now-moved file, in the working tree.  The pointer is (on a Unix system) a symlink to the now-moved file in the `.git/annex` directory.

(Some systems, such as Windows by default, can't use symbolic links; in this
case Git-Annex can use pointer files).

It is these pointers (usually symbolic links) that we check into the Git
repository.

## Git-Annex remotes

Git-Annex has *remotes*.  Remotes are stores for GAOs.

This can be confusing, because:

* Git-Annex can re-use ordinary Git repositories for this purpose.  In this
  case the remote in the Git-Annex sense can also be a remote in the Git sense.
* But Git-Annex also has the concept of a *special remote*, that is not a Git
  repository, and therefore cannot be a remote in the Git sense. Special
  remotes have various types of storage backing and interfaces, such as
  `rclone` pointing to Google Drive and so on.

I'll call both Git re-used repositories, and special remotes — Git-Annex
Remotes (GARs) — because they have the specific purpose of storing the GAOs.
GARs are pointers to particular data stores that can store GAOs.

Each GAR has a Universally Unique Identifier (UUID), so that Git-Annex can
record which of its remotes has each of the potential GAOs.

As this implies, any one individual GAR need not store all possible GAOs - it
might have a subset.  Git-Annex has to keep track of this information, so it
can `git annex get` any files that the user asks for, that they do not already
have in their `.git/annex` GAO object store.

Here is the confusion — your local Git repository also functions as a GAR — and
has its own UUID.  That is because, on your machine, after you `git annex add`
(or, as you see later `git annex get`) a large file, your own local `.git`
directory will have a copy of the GAO — in `.git/annex/objects`.  So Git-Annex
has to know that you also have a copy of the file, in your `.git/annex/objects`
directory, so you or your collaborators can ask for a copy of the file from
you, if they need to (using `git annex get` etc).

To say it again - a GAR is a different thing from a standard Git remote.  It is
specifically a place that Git-Annex can store or retrieve GAOs. Your local
`.git` repository store is one such place, so it also functions as a GAR, from
which you, or other people connected to your network, can get GAOs.

## Git-Annex metadata

Git-Annex makes and uses its own branch named `git-annex` to store metadata
about the location of GAOs within the known remotes.  We'll come across that
branch in the walkthrough below.

## Walkthrough

### Start with standard Git

Make a new directory for the Git repository, that will soon also be
Git-Annex-enhanced.

```{code-cell}
:tags: [remove-cell]

# Clean up any prior runs before we start.
if [ -d annex-repos ]; then
    # Work round git annex permission guards.
    chmod -R u+rwX annex-repos
    rm -rf annex-repos
fi

# Start in the annex-repos directory (we'll make several
# directories there).
mkdir annex-repos
cd annex-repos
```

```{code-cell}
mkdir my-repo
cd my-repo
```

When we do `git init` we have the usual `.git` subdirectories — this is, so
far, a normal Git repository.

```{code-cell}
git init
ls .git
```

```{code-cell}
tree .git/objects
```

```{code-cell}
echo "Some text" > my_small_file
# Makes my_small_file into a Git object, stored in .git/objects
git add my_small_file
tree .git/objects
```

Make an ordinary Git commit.  This generates a new directory-listing object, and a new commit object — the usual Git behavior.[^git-objects]

[^git-objects]: This is nothing to do with Git-Annex, but if you review the
  hash filenames of two new Git objects,  you'll see that one of them starts
  with the same short (7 character) hash given for the commit — that is the
  commit object. The other is the directory listing.

```{code-cell}
git commit -m "Added first file"
tree .git/objects
```

We only have one branch - the default `main` branch:

```{code-cell}
git branch -a
```

Here's the current (default) `.git/config` file.  Remember, this file is local to the repository, and does not get pushed with a `git push`.  Notice here there is no `[annex]` section.

```{code-cell}
cat .git/config
```

By default, Git doesn't have a `pre-commit` file in `hooks`.  We'll see later that Git-Annex adds one.

```{code-cell}
ls .git/hooks
```

### Add Git-Annex features with `git annex init`

Now we overlay the Git-Annex stuff on the normal Git repository:

```{code-cell}
git annex init
```

Notice that we now have a new `annex` directory in the `.git` directory.

```{code-cell}
ls .git
```

`.git/annex` doesn't have any objects yet, just some housekeeping files.

```{code-cell}
tree .git/annex
```

We also have a new `git-annex` branch:

```{code-cell}
git branch -a
```

Next we look at `git annex info` to show the Git-Annex-Remotes:

```{code-cell}
git annex info
```

For the moment, notice the "semitrusted repositories".  These are GARs - places
that Git-Annex knows can be sources or destinations for the Git-Annex-Object
files.  The first two (`web` and `bittorrent`) are generic sources
corresponding to URLs, and bittorrent files, but we'll ignore these for now.
The third points to the local `.git` directory.  This is a "remote" in a rather
confusing sense - that is - it's a place that can serve as a source for the
files that Git-Annex will store (the GAOs).   It's a remote in the sense that
other Git-Annex overlaid repositories may be able to use to get those files.
You can think of it as a remote to *other repositories*, and a local store to
this one.

After `git annex init`, the `.git/config` file has an `[annex]` section that
identifies this repository store (set of files on disk) with its new UUID.

```{code-cell}
cat .git/config
```

Git-Annex has added a `pre-commit` and other `hooks` to allow it to intercept and modify Git commands.

```{code-cell}
ls .git/hooks
```

### Adding files with `git annex add`

Now we'll add some potentially large file, using `git annex add`.  That is going to make a Git-Annex Object (GAO), and leave a pointer (symlink) behind in the working directory.

First we make a file that we will pretend is large.  We'll also calculate its SHA1 sum - you'll see why later.

```{code-cell}
echo "Something really large" > my_large_file
shasum my_large_file
```

Now we make that large file into a Git-Annex Object with `git annex add`:

```{code-cell}
git annex add my_large_file
```

Notice now that:

* The file has moved to `.git/annex/objects`.
* The moved file is now read-only (to prevent you accidentally overwriting it
  — see
  [lock](https://git-annex.branchable.com/git-annex-lock/)/[unlock](https://git-annex.branchable.com/git-annex-unlock/)).
* There's a symlink to that file in the working directory.
* Git-Annex added *the symlink* (and not the file itself) to the ordinary Git
  staging area.

In order:

```{code-cell}
# It's the same file exactly as the one previously in the working directory.
shasum .git/annex/objects/*/*/*/*
```

```{code-cell}
# The moved file is read-only to prevent accidental overwrites.
ls -al .git/annex/objects/*/*/*/*
```

```{code-cell}
# The file in the working tree has become a symlink.
ls -al my_large_file
```

```{code-cell}
# The symlink has been added to the Git staging area.
git status
```

`git annex list` tells us which GAR has each GAO.  `here` is the name for the local GAR, in `.git/annex`:

```{code-cell}
git annex list
```

We can now do a commit - but notice - the thing that gets added to the standard Git history, and stays in `.git/objects`, is nothing but the symlink:

```{code-cell}
git commit -m "Add link to my_large_file"
```

`git show` below identifies the symlink with the file mode 120000:

```{code-cell}
# Show contents of last commit.
git show main
```

To recap - the Git `.git/objects` directory never got a copy of
`my_large_file`.  The content of `my_large_file` belongs to Git-Annex, and is
stored in the `.git/annex/objects` directory, that does not get transferred
when you `git push`, or you `git clone` the repository.  Git itself only has
the symbolic link to the file.  But as we'll see soon, it does know where
copies of `my_large_file` live, through the information in the `git-annex`
branch.

### Clones and Git-Annex

To illustrate, if we do a typical clone of this `my-repo` repository, we do not
have the contents of `my_large_file`; we only have the symlink:

```{code-cell}
cd ..
# Simulate pushing to some upstream service such as Github.
git clone --bare my-repo my-repo-upstream.git
# Simulate cloning from there.
git clone my-repo-upstream.git my-repo-clone
cd my-repo-clone
```

We have put ourselves into the usual situation, where we've done a `git push`
to a remote service, and then done a `git clone` from the remote service, to
another computer.  After doing that:

```{code-cell}
# No .git/annex directory in the clone.
ls .git
```

```{code-cell}
# But we do have access to the remote git-annex branch, which maps
# repositories to GAOs.
git branch -a
```

```{code-cell}
# my_large_file is a broken symlink.
file my_large_file
```

If we try and fetch the file to which the symlink points, with `git annex get`,
Git-Annex can't do it, because it has no record (in the `git-annex` remote
branch) that the `origin` (upstream) repository has that file in its
`.git/annex` filesystem.

```{code-cell}
git annex list
```

### Fetching files with `git annex get`

However, the `git-annex` remote branch has told it where we might find the file
(see [Git-Annex internals](https://git-annex.branchable.com/internals)).
Notice the suggestion generated during the failure:

```{code-cell}
:tags: [raises-exception]

git annex get my_large_file
```

This message is telling us that we need to point directly to the original
repository as a source for the GAO files (in its `.git/annex` folder).

```{code-cell}
# Add the original repository as an ordinary Git remote.
git remote add original-repo ../my-repo --fetch
```

```{code-cell}
# Git-Annex now knows it can get the file.
git annex list
```

We ask Git-Annex to fetch the file.

```{code-cell}
git annex get my_large_file
```

```{code-cell}
# There are two repositories that Git-Annex knows have
# the file (in `.git/annex`) - this repo, and the original.
git annex list
```

```{code-cell}
# After git annex get, the symlink is fixed, because the file exists.
file my_large_file
```

## Copying annex files with `git annex copy`

```{code-cell}
# Make another pretend large file.
echo "More large" > another_large_file
# Calculate, store, show hash of file.
alf_hash=$(shasum another_large_file)
echo $alf_hash
```

```{code-cell}
# Add it to the Annex
git annex add another_large_file
# It's a symlink now.
ls -al another_large_file
```

```{code-cell}
git commit -m "Add another large file"
```

We have this file in `my-repo-clone`, but the original `my-repo` does not:

```{code-cell}
git annex list
```

```{code-cell}
# Notice we have the bytes of another_large_file
# (identified by the shasum, run above), as well as
# the original my_large_file
echo "SHA of another_large_file: $alf_hash"
echo "SHA of files in git annex objects directories:"
shasum .git/annex/objects/*/*/*/*
```

We can send our file to the original `my-repo`:

```{code-cell}
# Not there at the moment:
shasum ../my-repo/.git/annex/objects/*/*/*/*
```

```{code-cell}
git annex copy another_large_file --to original-repo
```

```{code-cell}
# It arrived.
shasum ../my-repo/.git/annex/objects/*/*/*/*
```

## The awe-inspiring power of `git annex sync`

+++

Let's add another file.

```{code-cell}
echo "More larger still" > yet_another_large_file
git annex add yet_another_large_file
git commit -m "Add yet another large file"
```

```{code-cell}
# This repo is the only one with this file.
git annex list
```

```{code-cell}
# The current known git branches
git fetch original-repo  # In fact this has not changed.
git branch -av
```

I'm now going to run [git annex sync](https://git-annex.branchable.com/sync/) without qualification.  This does a rather extreme Git and Git-Annex synchronization of this repository with the other repositories known to Git-Annex.

Read the linked documentation page.  Usually, with Git, you do not push directly to remotes, other than a single source-of-truth remote, and that remote is typically a `--bare` remote - it does not have a working tree.  If it does have a working tree, Git will, by default, warn you about this and decline, because it is so easy for the branch to get out of sync with the working tree.

However, Git-Annex `sync`, by default, takes a different approach - as it is so common to want to keep both Git history and the Git-Annex files in sync between repositories.

As you'll see in the linked documentation, by default, Git-Annex applies a synchronization scheme devised by Joachim Breitner, involving a special set of branches with names starting `synced/`.  As we're currently on the `main` branch, the corresponding `synced/` branch is `synced/main`.

In particular `git annex sync`, by default, does the following:

1. Automatically commits any changes in the working tree (configure with the
   `annex.autocommit` setting, see below).
1. Merges the `synced/main` branch (in our case) (if we have one) into `main`.
   This pulls in any Git history and files that a previous `git annex sync`
   pushed into our repository.  In our case, we do not have such a branch,
   because no-one has done a `git annex sync` to us.
2. Fetches from each remote, and merges in any changes from other remotes.
3. Pushes (in our case) `main` directly to any remotes.  Where Git prevents
   pushing to a branch with a working tree, it instead pushes to `synced/main`
   (in our case).
4. Copies any annexed files that the remote repository "wants".  "Wanting" is
   something you need to configure per repository.  We haven't done that yet, so no content gets copied

```{code-cell}
git annex sync
```

We note, and then ignore, that the repos to which we have synced now have `synced/git-annex` branches.   This is not important for our purposes.

Notice too that the original repo (but not the upstream `origin` repo) has
a new branch `synced/main`, because here, as is the default, Git did not allow
a push directly to the current branch of a non-bare repository (a repository
with a working tree).

```{code-cell}
git branch -av
```

In our case, sync does not copy the annex content to the original repository, because we haven't told Git-Annex that that remote "wants" these files yet.

```{code-cell}
git annex list
```

Let's configure the wanted setting for the original repository:

```{code-cell}
git annex wanted original-repo "include=*_large_file"
```

Re-run `git annex sync`, now Git-Annex knows the file is wanted:

```{code-cell}
git annex sync
git annex list
```

## You might want to constrain `git annex sync`

+++

First, you might have noted the first step in the sync above; `git annex sync`, by default, automatically does a commit of any changes to the working tree before it starts.

We make some staged and unstaged changes to the working tree:

```{code-cell}
# Show the last commit
git log -1
```

```{code-cell}
# Make a new file
echo "A file" > a_file
# Stage it.
git add a_file
# Make some more unstaged changes to file.
echo "Another line" >> a_file
git status
```

Now:

```{code-cell}
git annex sync
```

```{code-cell}
# Sync committed the staged and unstaged changes.
git status
```

```{code-cell}
# We have a new automated commit.
git log -1
```

You will see that sync made a new commit for you.   You might want that, but I do not, and I turn it off thus:

```{code-cell}
# Don't do automatic worktree commits.
git annex config --set annex.autocommit false
```

Now back to the merges.  As you can imagine, whenever you push directly into
another branch, with a history that is not fast-forward, you can get merge
conflicts. That means that, if you are not careful, `git annex sync` will
generate merge conflicts, either pulling into our repo, or pushing into
another.  As usual, merge conflicts can be obscure and difficult to resolve.
These forced merges also make it harder to think about what Git is doing, and
for many of us, that makes the process more obscure.  Combining the possibility
of merge conflicts with Git-Annex as an extra layer on top of Git, makes things
even more difficult.

Therefore, I suggest that you, like me, tell Git-Annex not to apply this synced
merge strategy, and instead, do Git pushes manually.

We make another commit just for the illustration:

```{code-cell}
echo "Yet another another" > yet_yet_another_large_file
git annex add yet_yet_another_large_file
git commit -m "Another another large file"
```

You can turn off Git-Annex' synced merge behavior for your repository with:

```{code-cell}
# Sync content only, not Git branches.
git annex config --set annex.synconlyannex true
```

Now:

```{code-cell}
git annex sync
```

Notice that the commit didn't get sent to the remotes, but the large file did:

```{code-cell}
git branch -av
```

```{code-cell}
git annex list
```

We send the commit manually:

```{code-cell}
git push origin main
```

# The special remotes

As you have seen, Git-Annex can use Git repositories on filesystems as storage
for GAOs — in the repository `.git/annex` directory.

But Git-Annex can also have *special remotes*, that have no necessary relationship to Git repositories.  For example, they can work with directories on file-sharing systems such as Dropbox and Google Drive.

You create special remotes with the `git annex initremote` command.

I say special remotes have no necessary relationship to Git repositories, but you can also label a Git repository as a special remote, using the `--type git` flag to `git annex initremote`.  Read the note below for more detail.

::: {note}

By the way, I hate to be confusing, but you will have seen above (with
`../my-repo`), that Git-Annex can identify repositories as capable of storing
annex files — a sort of special-remote-in-practice — and it can do this when it
has some way to read the `.git/config` of the repository, as it can, for
example when the repository is on the local file-system.  It uses `.git/config`
to work out what the UUID is of the remote repository.  Adding the repository
explicitly as a special remote, with `git annex initrepo --type git`, stores
the UUID in the `git-annex` branch, along with some useful location (such as
SSH path, filesystem path, etc).  When other repositories clone or otherwise
update their `git-annex` branch with this information, they can see the stored
UUID, and therefore use that remote as a Git-Annex special remote.

:::

You can enable known and already-configured special remotes with `git annex
enableremote <remotename>`.  This tells the local repository that you want to
be able to use that remote to fetch and store annex files, with `sync` and
other commands.

I don't cover special remotes further here, but see the [Git-Annex page on
special remotes](https://git-annex.branchable.com/walkthrough/#index12h2), and
the [doc page on special
remotes](https://git-annex.branchable.com/special_remotes).

## Which files go where

Consider setting `annex.largefiles` entries with `git annex config`, or in your
`.gitattributes` file, to tell Git-Annex which files it should handle (as GAOs)
and which Git should handle.  See the [annex.largefiles
page](https://git-annex.branchable.com/tips/largefiles) for details.  Note that
`annex.largefiles` just identifies files that Git-Annex should handle.  You can
use values for `annex.largefiles` to make Git-Annex always operate on files
larger than a particular size, but you can also use that setting to configure
Git / Git-Annex to select files by path name.

Consider using `git annex wanted` commands (see above) to tell Git-Annex which
remotes should house which files.   These rules get stored in the `git-annex`
branch. See the [Git-Annex wanted
page](https://git-annex.branchable.com/git-annex-wanted) for more.

## Whither Git-Annex

That was a tour of the basics.  You might now want to have a look at the
primary Git-Annex pages.

* The [main Git-Annex
  walkthrough](https://git-annex.branchable.com/walkthrough)
* [Git-Annex internals](https://git-annex.branchable.com/internals)
* [Scientific computing Git-Annex
  tutorial](https://scicomp.aalto.fi/scicomp/git-annex/)
