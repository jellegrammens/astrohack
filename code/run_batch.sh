#!/usr/bin/env bash

# writes the extracted features to files
# run with arguments: subfolder (Train/Test), number of parallel processes, number of files per batch
# add -t to print xargs command

ls /scratch/leuven/sys/ASTROHACK_DATA/$1 | grep -F 'g.csv' | xargs -P $2 -n$3 python2.7 code/batch.py -i $1 -a