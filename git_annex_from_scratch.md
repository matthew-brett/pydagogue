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

# Git-annex from scratch

I found I missed an under-the-hood explanation of what git-annex added on top
of an ordinary Git repository.

I'm partly starting from [Joey Hess' talk](https://www.youtube.com/watch?v=zQTAeX4prZo).

Here is a set of fundamental objects for git-annex, from that talk:

## Git-annex objects (GAOs)

GAOs are objects in the same sense that Git stores *objects* in its object
store.

For Git, when we do `git add myfile`, Git takes the contents of `myfile` (well,
in fact, a compressed version of `myfile`) and copies it into the
`.git/objects` directory, with a filename generated from the SHA1 hash of the
object.  In summary `git add myfile` causes a compressed *copy* of the file to
be written into `.git/objects` with a filename from its hash.

However, git-annex is designed to work with very large files that should not be
compressed or copied.  So when you create a git-annex object (with `git annex
add mybigfile`):

* The file is *moved* not copied
* Within the working tree, Git-annex leaves behind a pointer (usually
  a symbolic link) to the now-moved file.  See below.
* The moved file is not compressed
* The contents go into `.git/annex/objects` instead of `.git/objects`.
* There are different rules for making the hash filename, that we don't need to
  worry about for now.

## Git annex pointers

Above, we said that when we make a file into a Git-annex object, we leave
a *pointer* to the now-moved file, in the working tree.  The pointer is (on a Unix system) a symlink to the now-moved file in the `.git/annex` directory.

(Some systems, such as Windows by default, can't use symbolic links; in this
case Git-annex can use pointer files).

It is these pointers (usually symbolic links) that we check into the Git
repository.

## Git annex remotes

Git-annex has *remotes*. I'll call these Git-Annex Remotes (GARs) because they
function in a somewhat different way to standard Git remotes.  GARs are
pointers to particular data stores, that can store the GAOs.  These remotes can
Git-annex *special* remotes, not related to standard Git remotes, that have
various types of storage backing and interfaces, such as `rclone` pointing to
Google Drive and so on.

Each remote used with Git-annex has a Universally Unique Identifier (UUID), so that Git-annex can record which remote has each of the potential GAOs.

As this implies, a GAR need not store all possible GAOs - it might have a subset.  Git-annex has to keep track of this information, so it can `git annex get` any files that the user asks for, that they do not already have in their `.git/annex` GAO object store.

Now - your ordinary Git remote — for example `origin` — also functions as
a GAR - and has its own UUID.  That is because, on your machine,
after you `git annex add` (or, as you see later `git annex get`) a large file,
your own local `.git` directory will have a copy of the GAO — in
`.git/annex/objects`.  So Git-annex has to know, and may advertise to your
collaborators, that you also have a copy of the file, in your
`.git/annex/objects` directory.

To be clear - a GAR is a different thing from a standard Git remote.  It is specifically a place that Git annex can store or retrieve GAOs.

But, confusingly, your local `.git` repository store is one such place, that you can store GAOs (in `.git/annex`), so it, also functions as a GAR, from which you, or other people connected to your network, can get GAOs.

## Git annex metadata

Git-annex makes and uses its own branch to store metadata about the location of
GAOs within the known remotes.

## Walkthrough

Make a new directory for the git repository, that will soon also be
git-annex-enhanced.

```{code-cell}
:tags: [hide-input]

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

When we do `git init` we have the usual `.git` directories — this is, so far, a normal Git repository.

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

Make an ordinary Git commit.  This generates a new directory-listing object, and a new commit object.

This is basic Git machinery, but notice that the listed (short) commit hash
corresponds to one of the two new objects.  The other is the directory listing.

```{code-cell}
git commit -m "Added first file"
tree .git/objects
```

We only have one branch - the default `main` branch:

```{code-cell}
git branch -a
```

Now we overlay the Git-annex stuff on the normal Git repository:

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

For the moment, notice the "semitrusted repositories".  These are GARs - places that Git-Annex knows can be sources of the Git-Annex-Object files.  The first two (`web` and `bitorrent`) are generic sources corresponding to URLs, and bitorrent files, but we'll ignore these for now.  The third points to the local `.git` directory.  This is a "remote" in a rather confusing sense - that is - it's a place that can serve as a source for the files that Git-annex will store (the GAOs).   It's a remote in the sense that other Git-annex overlaid repositories may be able to use to get those files.  You can think of it as a remote to *other repositories*, and a local store to this one.

+++

Now we'll add some potentially large file, using `git annex add`.  That is going to make a Git Annex Object (GAO), and leave a pointer (symlink) behind in the working directory.

First we make a file, that we will pretend is large.  We'll also calculate its SHA1 sum - you'll see why later.

```{code-cell}
echo "Something really large" > my_large_file
shasum my_large_file
```

Now we make that large file into a Git Annex Object with `git annex add`:

```{code-cell}
git annex add my_large_file
```

Notice now that:

* The file has moved to `.git/annex/objects`
* There's a symlink to that file in the working directory.
* Git annex added *the symlink* (and not the file itself) to the ordinary git staging area.

In order:

```{code-cell}
shasum .git/annex/objects/*/*/*/*
```

```{code-cell}
ls -al my_large_file
```

```{code-cell}
git status
```

`git annex list` tells us which GAR has each GAO.  `here` is the name for the local GAR, in `.git/annex`:

```{code-cell}
git annex list
```

We can now do a commit - but notice - the thing that gets added to the standard git history, and stays in `.git/objects`, is nothing but the symlink:

```{code-cell}
git commit -m "Add link to my_large_file"
```

`git show` below identifies the symlink with the file mode 120000:

```{code-cell}
# Show contents of last commit.
git show main
```

To recap - Git itself never got a copy of `my_large_file`.  The contents of `my_large_file` belongs to Git annex, and is stored in the `.git/annex` directory, that does not get transferred when you clone the repository.  Git itself only has the symbolic link to the file.  But as we'll see soon, it does know where copies of `my_large_file` live, through the information in the `git-annex` branch.

To illustrate, if we do a direct clone of this `my-repo` repository, we do not have the contents of `my_large_file`; we only have the symlink:

```{code-cell}
cd ..
# Simulate pushing to some upstream service such as Github.
git clone --bare my-repo my-repo-upstream.git
# Simulate cloning from there.
git clone my-repo-upstream.git my-repo-clone
cd my-repo-clone
```

```{code-cell}
# No .git/annex directory in the clone.
ls .git
```

```{code-cell}
# But we do have access to the git-annex branch, which maps
# repositories to GAOs
git branch -a
```

```{code-cell}
# my_large_file is a broken symlink
file my_large_file
```

If we try and fetch the file to which the symlink points, with `git annex get`, Git annex doesn't know where to find it, because it has no record of the `origin` (upstream) repository having it:

```{code-cell}
git annex list
```

However, the `git-annex` branch does tell it where we might find it - notice the suggestion generated during the failure.

```{code-cell}
:tags: [raises-exception]

git annex get my_large_file
```

This is telling us that we need to point directly to the original repository as a source for the GAO files:

```{code-cell}
# Add the original repository as an ordinary Git remote.
git remote add original-repo ../my-repo --fetch
```

```{code-cell}
# Git annex now knows it can get the file.
git annex list
```

We ask Git annex to fetch the file.

```{code-cell}
git annex get my_large_file
```

```{code-cell}
# There are two repositories that Git annex knows has
# the file (in `.git/annex`) - this repo, and the original.
git annex list
```

```{code-cell}
# The symlink is now fixed.
file my_large_file
```

## Whence Git annex

That was a tour of the basics.  You might now want to have a look at:

* [The main git-annex
  walkthrough](https://git-annex.branchable.com/walkthrough/)
* [git-annex
  internals](https://web.archive.org/web/20260725205005/https://git-annex.branchable.com/internals/)
  (Archive.org link, the source page was down at time of writing).
