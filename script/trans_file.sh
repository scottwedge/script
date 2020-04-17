#!/bin/bash

files=$(ls -lt | grep -v total | gawk '{print $NF}' | head -n ${1:-5})
n=0
for file in $files
do
	n=$[$n + 1]
	echo $n $file
done

read id

n=0
for file in $files
do
	n=$[$n + 1]
	if [ ${id} -ge ${n} ]
	then
	    echo start ssh $file
	    #echo y_spl $file	
	    y_spl $file	
	    echo end ssh $file
	fi
done
