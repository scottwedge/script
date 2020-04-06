#!/bin/bash


for i in `cat irdb.txt| cut -d : -f 4`
do
    hping3 -c 1 -S -p 1024 -a $i 11.1.2.2 &
    #echo hping3 -c 1 -S -p 1024 -a $i 11.1.2.2
done


#cut -d : -f 4 irdb.txt  | xargs -n 1 -P 0 -I {} hping3 11.1.2.2 -c 1 -S -a {} -p 1024
