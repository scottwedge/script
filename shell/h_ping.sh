#!/bin/bash

cmd="hping3 11.1.2.2 -c 1"
flag=0
if [ -z $1 ]
then
    cmd="$cmd -S"
else
    while [ -n "$1" ]
    do
       if [ $1 == "-a" ]
       then
           flag=1
       fi
       if [ ${flag} -eq 1 ] && [ $1 != "-a" ]
       then
          sip=${1} 
          flag=0
       fi
       cmd="$cmd $1"
       shift
    done
fi

if [ -n "${sip}" ]
then
    ip addr add ${sip}/24 dev eth1
fi

echo $cmd
result=$($cmd 2>&1) 


if [[ $result =~ "1 packets received, 0% packet loss" ]]
then
    echo "ok"
else
    echo "fail"
fi


if [ -n "${sip}" ]
then
    ip addr del ${sip}/24 dev eth1
fi
