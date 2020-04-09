#!/bin/bash

while getopts :ab:c:d opt
do
	case "${opt}" in
		a) echo "option a";;
		b) echo "option b $OPTARG";;
		c) echo "optin c $OPTARG";;
		d) echo "optin d";;
		*) echo "unkonw option $opt";;
	esac
done

shift $[ $OPTIND - 1 ]

for i in "$@"
do
	echo para: $i
done
