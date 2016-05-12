#!/bin/bash
# Move directories to values given by sha1sum
NAMES_FILE=".names2sha"
rm -rf $NAMES_FILE
for var in */message.txt; do
    dname=$(dirname $var)
    sha_val=$(shasum $var | awk '{print $1}')
    mv $dname $sha_val
    echo "$dname $sha_val" >> $NAMES_FILE
done
