#!/bin/bash

cut -d : -f 4 irdb.data  | xargs -n 1 -P 0 -I {} hping3 1.2 -c 1 -S -a {} -p 1024

: '
for i in `cat irdb.data | cut -d : -f 4`
do
    hping3 -c 1 -S -p 1024 -a $i 11.1.2.2 &
    #echo hping3 -c 1 -S -p 1024 -a $i 11.1.2.2 
done

'
