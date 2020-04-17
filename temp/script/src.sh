#!/bin/bash
src=${1:-1.1.1.1}
ip addr flush scope global dev lo
ip addr add $src/32 dev lo
#curl 11.1.2.1 --interface lo 
ping 11.1.2.1 -I $src -c 1 -W 1
