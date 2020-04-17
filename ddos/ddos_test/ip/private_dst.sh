cat /home/ddos/ip/$1 | xargs -n 1 -I {} sh /home/script/dst.sh {}
