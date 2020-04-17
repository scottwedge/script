#!/bin/bash


if [ -z "$1" ]
then
	echo 1
	./ntp_normal_test.sh -i 1 version 
	./ntp_normal_test.sh -i 2 version 
	./ntp_normal_test.sh -i 1 stratum
	./ntp_normal_test.sh -i 2 stratum	
	./ntp_normal_test.sh -i 1 len
	./ntp_normal_test.sh -i 2 len
	./ntp_normal_test.sh -i 3 len
	./ntp_normal_test.sh -i 4 len
	./ntp_normal_test.sh -i 5 len
	./ntp_normal_test.sh -i 6 len
	./ntp_normal_test.sh -i 1 trans
	./ntp_normal_test.sh -i 2 trans
	./ntp_normal_test.sh -i 3 trans
	./ntp_normal_test.sh -i 4 trans
	./ntp_normal_test.sh -i 1 unsol
	./ntp_normal_test.sh -i 1 mode
else
	echo 2
	./ntp_normal_test.sh -i 1 -a version 
	./ntp_normal_test.sh -i 2 -a version 
	./ntp_normal_test.sh -i 1 -a stratum
	./ntp_normal_test.sh -i 2 -a stratum	
	./ntp_normal_test.sh -i 1 -a len
	./ntp_normal_test.sh -i 4 -a len
	./ntp_normal_test.sh -i 5 -a len
	./ntp_normal_test.sh -i 6 -a len
	./ntp_normal_test.sh -i 1 -a mode
fi
