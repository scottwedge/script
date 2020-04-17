#!/bin/bash
dst=${1:-1.0.0.2}
src=${2:-1.0.0.1}
sshpass -p fortinet ssh root@10.0.200.163 "ip addr flush scope global dev lo;ip addr add ${dst}/32 dev lo"
#route add -net $dst netmask 255.255.255.255 gateway 11.1.2.1
ip addr flush scope global dev lo
ip addr add ${src}/32 dev lo
#curl 11.1.2.1 --interface $1
#ping $dst -I ${src} -c 1 -W 1
hping3 ${dst} -a ${src} -S -p 1024 -I eth1 -c 1
#route del -net $dst netmask 255.255.255.255 gateway 11.1.2.1
sshpass -p fortinet ssh root@10.0.200.163 "ip addr flush scope global dev lo"
