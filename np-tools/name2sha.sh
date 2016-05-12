#!/bin/bash
# Return sha corresponding to previous directory name as argument
NAMES_FILE=".names2sha"
while read p; do
   name=$( echo $p | awk '{print $1}' )
   sha_val=$( echo $p | awk '{print $2}' )
   if [ "$name" == "$1" ]; then
       echo "$sha_val"
       break
   fi
done < $NAMES_FILE
