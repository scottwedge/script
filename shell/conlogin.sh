#!/bin/bash

for((i=0;i<$1;i++))
do
	echo $i
	sshpass -p f ssh a@10.0.100.114 -t 'exit' &
done

