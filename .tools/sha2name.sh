#!/bin/bash
# Return previous name corresponding to current sha, given as argument
NAMES_FILE=".names2sha"
while read p; do
   name=$( echo $p | awk '{print $1}' )
   sha_val=$( echo $p | awk '{print $2}' )
   if [ "$sha_val" == "$1" ]; then
       echo "$name"
       break
   fi
done < $NAMES_FILE
