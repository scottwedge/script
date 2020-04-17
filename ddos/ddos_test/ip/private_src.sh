cat $1 | xargs -n 1 -P 0 -I {} hping3 1.2 -c 1 -S -I eth1 -a {}
