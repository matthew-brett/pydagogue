#!/bin/bash
# Make tags from commit messages
# Remove old tags
for tag in $(git tag); do
    git tag -d $tag
done
# Make new tags from commit messages
for hash in $(git log --pretty="%h"); do
    msg=$(git log -1 --pretty="%s" $hash)
    $(git tag $msg -m $msg $hash)
done
echo Done.
