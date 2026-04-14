#!/bin/bash

# PURPOSE: 
# To automate the process of downloading and naming files from xano-canto while we build our training data.

# Running this script will download the page's associated mp3 file and save it with the convention 
#'common_name-species_name(cited source id).mp3' into the directory "trapped_birds_nest"


# HOW TO USE: 
# $ bash birdTrapper.sh 'pasted URL of xano-canto page'
# example URL: https://xeno-canto.org/1046354


URL=$1

# Grabs string from title element of supplied URL
PAGE_TITLE=$(curl -s $URL | awk -F '[<>]' '/<title>/{print $3}')

# REGEX formatted extraction for "common_name.species_name(xanoPage).mp3"
FILENAME=$(echo "$PAGE_TITLE" | sed -E 's/^([^ ]+) (.*) \((.*)\) ::.*/\2-\3(\1)/; s/ /_/g')


# comment this line out to utilize the trapped_birds_nest!
# curl -Ls "$URL/download" -o "$FILENAME.mp3"


# Uncomment this section to utilize the trapped_birds_nest!

# extracted .mp3s will go here
DEST_FOLDER="./trapped_birds_nest"

# trigger download and drop properly named .mp3 into the nest
mkdir -p "$DEST_FOLDER"
curl -Ls "$URL/download" -o "$DEST_FOLDER/$FILENAME.mp3"
