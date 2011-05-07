#!/bin/bash
# Commands to make git repository for rebase page

function make_repo {
    local repo_name=$1
    rm -rf $repo_name
    mkdir $repo_name
    cd $repo_name
    git init
}

function make_commit {
    local cname=$1
    local cfile=${cname}_file
    touch ${cfile}
    git add $cfile
    git commit -m "$cname"
}


# History 1
make_repo history1
make_commit D
git branch at-root
make_commit E
git co -b topic
make_commit A
make_commit B
make_commit C
git co master
make_commit F
make_commit G
cd ..

# Root example
make_repo root-example
make_commit A
make_commit B
make_commit C
make_commit D
# Make detached branch
git symbolic-ref HEAD refs/heads/other-branch
rm *
rm .git/index
make_commit X
make_commit Y
make_commit Z

