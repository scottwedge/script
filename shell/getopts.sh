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



#/bin/bash

pcapname=/home/pcap/ntp/ntp_private.pcap
yamldir=/home/tmp/module/ntp/

action=block
index=1

while getopts :bi: opt
do
	case "$opt" in
		b) action=forward;;
		i) index=$OPTARG;;
		*) echo "error option";;
	esac
done

shift $[ $OPTIND - 1 ]

type=${1}


if [ "${type}" = "version" ]
then
	if [ "$action" = "block" ]
	then
		case "$index" in
			1) echo block 1;;
			2) echo block 2;;
		esac
	else
		case "$index" in
			1) echo forward 1;;
			2) echo forward 2;;
		esac
	fi

fi
