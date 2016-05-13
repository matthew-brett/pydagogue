#!/bin/bash
# Move directories to values given by sha1sum
NAMES_FILE=".names2sha"
while read p; do
   name=$( echo $p | awk '{print $1}' )
   sha_val=$( echo $p | awk '{print $2}' )
   mv $sha_val $name
done < $NAMES_FILE
rm $NAMES_FILE
