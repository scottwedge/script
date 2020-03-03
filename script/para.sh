#!/bin/bash

#!/bin/bash
# Processing options & parameters with getopts
#
while getopts :a:u: opt
do

passwd=fortinet

case "$opt" in
a) addr=$OPTARG ;;
u) user=$OPTARG ;;
*) echo "Unknown option: $opt" ;;
esac
done
#
shift $[ $OPTIND - 1 ]

if [ -n "$1" ]
then
    csvname="devicelist.csv"
    while IFS=',' read -r id address username password
    do
      if [ "$1" = "${id}" ]
      then
          passwd=${password}
          addr=${address}
          user=${username}

      fi
    done < "csvname.csv"
fi

cmd="sshpass -p "$passwd" ssh ${user}@${addr}"
$cmd