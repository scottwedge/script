#!/bin/bash

set -- $(getopt ab:c "$@")
while [ -n "$1" ]
do
	case "$1" in 
		-a) echo "option -a ";;
		-b) echo "option $1 $2"
			shift;;
		-c) echo "option -c ";;
		--) shift
			break;;
		*) echo "$1 do not exist";;
	esac
	shift
done
for i in "$@"
do
	echo $i
done


