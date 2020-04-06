#!/bin/bash
timestap=$(date +%Y%m%d_%H%M%S)
pcapname=${timestap}.pcap
#filter="udp and ip host 1.0.0.2"
filter=${2}

./client.out "nohup tcpdump -i eth1 -nne -s 0 ${filter} -w /tmp/${pcapname} &> /dev/null &"

${1}

./client.out "killall -2 tcpdump"
./client.out "tshark -nn $3 -r /tmp/${pcapname}"


