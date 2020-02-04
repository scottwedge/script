#!/bin/bash

for((i=0;i<$4;i++))
do
    sshpass -p $3 ssh $2@$1 -t 'exit'
	echo $i
done

