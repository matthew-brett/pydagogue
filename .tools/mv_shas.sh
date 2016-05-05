#!/bin/bash
# Move directories to values given by sha1sum
for var in */message.txt; do
    dname=$(dirname $var)
    sha_val=$(shasum $var | awk '{print $1}')
    git mv $dname $sha_val
done
