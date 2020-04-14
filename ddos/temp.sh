#!/bin/bash

if [ "$1" = "1" ]
then
	python3 send_scapy.py "IP()/UDP(sport = 10000, dport = 123)/NTPControl(op_code = 1, count = 8, data=b'\x00' * 8, sequence = 0)"
	python3 send_scapy.py --direction outbound "IP()/UDP(dport = 10000, sport = 123)/NTPControl(response=1, status_word=NTPSystemStatusPacket(), op_code = 1, count = 8, data= b'\x00' * 8, more = 1, offset = 0)"
	python3 send_scapy.py --direction outbound "IP()/UDP(dport = 10000, sport = 123)/NTPControl(response=1, status_word=NTPSystemStatusPacket(), op_code = 1, count = 8, data= b'\x00' * 8, more = 1, offset = 8)"
	python3 send_scapy.py --direction outbound "IP()/UDP(dport = 10000, sport = 123)/NTPControl(response=1, status_word=NTPSystemStatusPacket(), op_code = 1, count = 8, data= b'\x00' * 8, more = 1, offset = 16)"
	python3 send_scapy.py --direction outbound "IP()/UDP(dport = 10000, sport = 123)/NTPControl(response=1, status_word=NTPSystemStatusPacket(), op_code = 1, count = 8, data= b'\x00' * 8, more = 0, offset = 24)"
elif [ "$1" = "2" ]
then
	python3 send_scapy.py "IP()/UDP(sport = 11000, dport = 123)/NTPControl(op_code = 1, count = 8, data=b'\x00' * 8, sequence = 0)"
	python3 send_scapy.py --direction outbound "IP()/UDP(dport = 11000, sport = 123)/NTPControl(response=1, status_word=NTPSystemStatusPacket(), op_code = 1, count = 8, data= b'\x00' * 8, more = 1, offset = 1)"
elif [ "$1" = "3" ]
then
	echo client 1
	python3 send_scapy.py "IP()/UDP(sport = 12000, dport = 123)/NTPControl(op_code = 1, count = 8, data=b'\x00' * 8, sequence = 0)"
	sleep 3
	echo server1
	python3 send_scapy.py --direction outbound "IP()/UDP(dport = 12000, sport = 123)/NTPControl(response=1, status_word=NTPSystemStatusPacket(), op_code = 1, count = 8, data= b'\x00' * 8, more = 0, offset = 16)"
	sleep 3
	echo server2
	python3 send_scapy.py --direction outbound "IP()/UDP(dport = 12000, sport = 123)/NTPControl(response=1, status_word=NTPSystemStatusPacket(), op_code = 1, count = 8, data= b'\x00' * 8, more = 1, offset = 0)"
	sleep 3
	echo server3
	python3 send_scapy.py --direction outbound "IP()/UDP(dport = 12000, sport = 123)/NTPControl(response=1, status_word=NTPSystemStatusPacket(), op_code = 1, count = 8, data= b'\x00' * 8, more = 1, offset = 8)"	
elif [ "$1" = "4" ]
then
	echo client 1
	python3 send_scapy.py "IP()/UDP(sport = 13000, dport = 123)/NTPControl(op_code = 1, count = 8, data=b'\x00' * 8, sequence = 0)"
	sleep 3
	echo server1
	python3 send_scapy.py --direction outbound "IP()/UDP(dport = 13000, sport = 123)/NTPControl(response=1, status_word=NTPSystemStatusPacket(), op_code = 1, count = 8, data= b'\x00' * 8, more = 0, offset = 16)"
	sleep 3
	echo server2
	python3 send_scapy.py --direction outbound "IP()/UDP(dport = 13000, sport = 123)/NTPControl(response=1, status_word=NTPSystemStatusPacket(), op_code = 1, count = 8, data= b'\x00' * 8, more = 1, offset = 0)"
	sleep 3	
	echo server3
	python3 send_scapy.py --direction outbound "IP()/UDP(dport = 13000, sport = 123)/NTPControl(response=1, status_word=NTPSystemStatusPacket(NTPErrorStatusPacket(error_code = (0,7))), op_code = 1, count = 14, data= b'\x00' * 14, more = 1, offset = 2)"	
fi


	#python3 send_scapy.py "IP()/UDP()/NTPControl(op_code = 1, count = 8, data=b'\x00' * 8, sequence = 0)"
	#python3 send_scapy.py --direction outbound "IP()/UDP()/NTPControl(response=1, status_word=NTPSystemStatusPacket(), op_code = 1, count = 8, data= b'\x00' * 8, more = 1, offset = 0)"
	#python3 send_scapy.py --direction outbound "IP()/UDP()/NTPControl(response=1, status_word=NTPSystemStatusPacket(), op_code = 1, count = 8, data= b'\x00' * 8, more = 1, offset = 8)"
	#python3 send_scapy.py --direction outbound "IP()/UDP()/NTPControl(response=1, status_word=NTPSystemStatusPacket(), op_code = 1, count = 8, data= b'\x00' * 8, more = 1, offset = 16)"
	#python3 send_scapy.py --direction outbound "IP()/UDP()/NTPControl(response=1, status_word=NTPSystemStatusPacket(), op_code = 1, count = 8, data= b'\x00' * 8, more = 0, offset = 24)"
