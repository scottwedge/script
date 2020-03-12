#!/bin/bash

cut -d : -f 4 1.txt  | xargs -n 1 -P 0 -I {} hping3 11.1.2.2 -c 1 -S -a {} -p 1024


