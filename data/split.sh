#!/bin/bash

TAR=$4 # target directory
INP=$3 # input file
SIZ=$2 # partition size
NOP=$1 # number of partitions

for IDX in $(seq $NOP) ; do

OUT="$(printf "%03d" $IDX).tic" ; echo $OUT ;
QQQ=$(echo "$IDX*$SIZ" | bc) ;
head -n $QQQ $INP | tail -n $SIZ > "$TAR/$OUT" ;

done
