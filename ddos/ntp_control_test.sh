#/bin/bash

pcapname=/home/pcap/ntp/ntp_private.pcap
yamldir=/home/tmp/module/ntp/

action=block
index=1

while getopts :ai: opt
do
	case "$opt" in
		a) action=forward;;
		i) index=$OPTARG;;
		*) echo "error option";;
	esac
done

shift $[ $OPTIND - 1 ]

type=${1}

#"""

case "${type}" in 
	version)
		if [ "$action" = "block" ]
		then
			case "$index" in
				1) 
					python3 send_scapy.py "IP()/UDP(sport = RandNum(1024,65536))/NTPControl(op_code = 1, count = 8, data=b'\x00' * 8,version = [(0, 1), 5])"
					;;
			esac
		else
			case "$index" in
				1) 
					python3 send_scapy.py "IP()/UDP(sport = RandNum(1024,65536))/NTPControl(op_code = 1, count = 8, data=b'\x00' * 8,version = [(2,4)])"
					;;
			esac
		fi
	;;		
	trans)
		if [ "$action" = "block" ]
		then
			case "$index" in
				1) 
					python3 send_scapy.py "(IP()/UDP(sport = 10000)/NTPControl(op_code = [1, 1], count = 8, data=b'\x00' * 8))"
					;;
			esac
		else
			case "$index" in
				1) 
					python3 send_scapy.py "IP()/UDP(sport = 20000)/NTPControl(op_code = [1, 2], count = 8, data=b'\x00' * 8)"
					;;
			esac
			case "$index" in
				2) 
					python3 send_scapy.py "IP()/UDP(sport = [30000, 30001])/NTPControl(op_code = 1, count = 8, data=b'\x00' * 8)"
					;;
			esac			
			case "$index" in
				3) 
					python3 send_scapy.py "IP()/UDP(sport = 40000)/NTPControl(op_code = 1, association_id = [1, 2], count = 8, data=b'\x00' * 8)"
					;;
			esac				
		fi		
	;;
	seq)
		if [ "$action" = "block" ]
		then
			case "$index" in
				1) 
					python3 send_scapy.py "IP()/UDP(sport = 50000)/NTPControl(op_code = 1, count = 8, data=b'\x00' * 8, sequence = 0)"
					python3 send_scapy.py --direction outbound "IP()/UDP(dport = 50000)/NTPControl(response=1, status_word=NTPSystemStatusPacket(), op_code = 1, count = 8, data=b'\x00' * 8, sequence = 1)"
				    python3 send_scapy.py "IP()/UDP(sport = 51000)/NTPControl(op_code = 1, count = 8, data=b'\x00' * 8, sequence = 2)"
					python3 send_scapy.py --direction outbound "IP()/UDP(dport = 51000)/NTPControl(response=1, status_word=NTPSystemStatusPacket(), op_code = 1, count = 8, data=b'\x00' * 8, sequence = 3)"
					;;
			esac
		else
			case "$index" in
				1) 
					python3 send_scapy.py "IP()/UDP(sport = 52000)/NTPControl(op_code = 1, count = 8, data=b'\x00' * 8, sequence = 0)"
					python3 send_scapy.py --direction outbound "IP()/UDP(dport = 52000)/NTPControl(response=1, status_word=NTPSystemStatusPacket(), op_code = 1, count = 8, data=b'\x00' * 8, sequence = 0)"
				    python3 send_scapy.py "IP()/UDP(sport = 53000)/NTPControl(op_code = 1, count = 8, data=b'\x00' * 8, sequence = 2)"
					python3 send_scapy.py --direction outbound "IP()/UDP(dport = 53000)/NTPControl(response=1, status_word=NTPSystemStatusPacket(), op_code = 1, count = 8, data=b'\x00' * 8, sequence = 2)"		
					;;
			esac	
		fi		
	;;	
	unsol)
		if [ "$action" = "block" ]
		then
			case "$index" in
				1) 
					python3 send_scapy.py --direction outbound "IP()/UDP(dport = 60000)/NTPControl(response=1, status_word=NTPSystemStatusPacket(), op_code = 1, count = 8, data=b'\x00' * 8, sequence = 0)"
				   	;;
			esac
		else
			case "$index" in
				1) 
					python3 send_scapy.py "IP()/UDP(sport = 61000)/NTPControl(op_code = 1, count = 8, data=b'\x00' * 8, sequence = 0)"
					python3 send_scapy.py --direction outbound "IP()/UDP(dport = 61000)/NTPControl(response=1, status_word=NTPSystemStatusPacket(), op_code = 1, count = 8, data=b'\x00' * 8, sequence = 0)"
					;;
			esac	
		fi		
	;;		
	reflect)
		if [ "$action" = "block" ]
		then
			case "$index" in
				1) 
					python3 send_scapy.py "IP()/UDP(sport = RandNum(1024,65536))/NTPControl(op_code = 1, count = 8, data=b'\x00' * 8,version = 2)"
					;;
			esac
		fi
	;;		
	len)
		if [ "$action" = "block" ]
		then
			case "$index" in
				1) # ntp len < 12, scapy ntp control have bug,default have 1 more bytes,so get [:-2]
					python3 send_scapy.py "IP()/UDP(sport=123, dport=123)/Raw(raw(NTPControl(op_code = 1, version = 2))[:-2])"
					;;
				2) # ntp len > 516 
					python3 send_scapy.py "IP()/UDP(sport = RandNum(1024,65536))/NTPControl(op_code = 1, count = 508, data=b'\x00' * 508)"
					;;		
				3) # ntp len % 4
					python3 send_scapy.py "IP()/UDP(sport = RandNum(1024,65536))/NTPControl(op_code = 1, count = 503, data=b'\x00' * 503)"
					;;
				4) # ntp count field + 12 > ntp len 
					python3 send_scapy.py "IP()/UDP(sport = RandNum(1024,65536))/NTPControl(op_code = 1, count = 504, data=b'\x00' * 500)"
					;;					
			esac
		else
			case "$index" in
				1) # ntp len = 12, scapy ntp control have bug,default have 1 more bytes,so get [:-1]
					python3 send_scapy.py "IP()/UDP(sport=123, dport=123)/Raw(raw(NTPControl(op_code = 1, version = 2))[:-1])"
					;;
				2|3) # ntp len > 516 
					python3 send_scapy.py "IP()/UDP(sport = RandNum(1024,65536))/NTPControl(op_code = 1, count = 504, data=b'\x00' * 504)"
					;;		
				4) # ntp count field + 12 <= ntp len 
					python3 send_scapy.py "IP()/UDP(sport = RandNum(1024,65536))/NTPControl(op_code = 1, count = [496, 500], data=b'\x00' * 500)"
					;;										
			esac			
		fi
	;;	

	control)
		if [ "$action" = "block" ]
		then
			case "$index" in
				1) #control mode request li can not be none
					python3 send_scapy.py "IP()/UDP(sport = RandNum(1024,65536))/NTPControl(op_code = 1, count = 8, data=b'\x00' * 8, zeros = 1)"
					;;
				2) #request error or more is set
					python3 send_scapy.py "IP()/UDP(sport = RandNum(1024,65536))/NTPControl(op_code = 1, count = 8, data=b'\x00' * 8, err = 1, more = 0)"
					python3 send_scapy.py "IP()/UDP(sport = RandNum(1024,65536))/NTPControl(op_code = 1, count = 8, data=b'\x00' * 8, more = 1, err = 0)"
					;;
				3) #Check NTP Control Request with none zero offset
					python3 send_scapy.py "IP()/UDP(sport = RandNum(1024,65536))/NTPControl(op_code = 1, count = 8, data=b'\x00' * 8, offset = 1)"
					;;
				4) #Check NTP Control Request with reserved OPCODE(0 or >7).
					python3 send_scapy.py "IP()/UDP(sport = RandNum(1024,65536))/NTPControl(count = 8, data=b'\x00' * 8, op_code = [0, 8])"
					;;
				5) #send NTP Control resposne with count values as 0 and more bit set.	
					python3 send_scapy.py --direction outbound "IP()/UDP(sport=123, dport=123)/NTPControl(response=1, status_word=NTPSystemStatusPacket(), count = 0, more = 1, data = '')"
					;;
				6) #1. First response with M=1 with non-zero OFFSET
					  python3 send_scapy.py "IP()/UDP(sport = 11000, dport = 123)/NTPControl(op_code = 1, count = 8, data=b'\x00' * 8, sequence = 0)"
                      python3 send_scapy.py --direction outbound "IP()/UDP(dport = 11000, sport = 123)/NTPControl(response=1, status_word=NTPSystemStatusPacket(), op_code = 1, count = 8, data= b'\x00' * 8, more = 1, offset = 1)"
					;;
				7) #Response with reserved STATUS values( >7)
                    python3 send_scapy.py --direction outbound "IP()/UDP()/NTPControl(response=1, err = 1, status_word=NTPErrorStatusPacket(error_code = 8),count = 8, data=b'\x00' * 8, op_code = 1)"
					;;					
			esac
		else
			case "$index" in
				1) #contrl mode request li should be none.response li can be not none
					python3 send_scapy.py "IP()/UDP(sport = 61000)/NTPControl(op_code = 1, count = 8, data=b'\x00' * 8, zeros = 0)"
					python3 send_scapy.py --direction outbound "IP()/UDP(sport = 123, dport = 61000)/NTPControl(response=1, status_word=NTPSystemStatusPacket(), op_code = 1, count = 8, data=b'\x00' * 8, sequence = 0, zeros = 1)"
					;;
				2) #request error or more is not set
					python3 send_scapy.py "IP()/UDP(sport = RandNum(1024,65536))/NTPControl(op_code = 1, count = 8, data=b'\x00' * 8, more = 0, err = 0)"
					;;
				3) #Check NTP Control Request with zero offset
					python3 send_scapy.py "IP()/UDP(sport = RandNum(1024,65536))/NTPControl(op_code = 1, count = 8, data=b'\x00' * 8, offset = 0)"
					;;
				4) #Check NTP Control Request with reserved OPCODE(1,6).
					python3 send_scapy.py "IP()/UDP(sport = RandNum(1024,65536))/NTPControl(count = 8, data=b'\x00' * 8, op_code = (1, 6))"
					;;
				5) #send NTP Control resposne not with count values as 0 and more bit set.
					python3 send_scapy.py --direction outbound "IP()/UDP(sport=123, dport=123)/NTPControl(response=1, status_word=NTPSystemStatusPacket(), op_code = 1, count = 8, data=b'\x00' * 8, more = 1)"
					python3 send_scapy.py --direction outbound "IP()/UDP(sport=123, dport=123)/NTPControl(response=1, status_word=NTPSystemStatusPacket(), count = 0, more = 0, data = '')"
					;;
				6) #First response with M=1 with non-zero OFFSET
                    python3 send_scapy.py "IP()/UDP(sport = 12000, dport = 123)/NTPControl(op_code = 1, count = 8, data=b'\x00' * 8, sequence = 0)"
                    python3 send_scapy.py --direction outbound "IP()/UDP(dport = 12000, sport = 123)/NTPControl(response=1, status_word=NTPSystemStatusPacket(), op_code = 1, count = 8, data= b'\x00' * 8, more = 1, offset = 0)"
					;;
				7) #Response with reserved STATUS values( >7)
                    python3 send_scapy.py --direction outbound "IP()/UDP()/NTPControl(response=1, err = 1, status_word=NTPErrorStatusPacket(error_code = (0,7)),count = 8, data=b'\x00' * 8, op_code = 1)"
					;;			
				8) #cache test.
					python3 send_scapy.py "IP()/UDP(sport = 10000, dport = 123)/NTPControl(op_code = 1, count = 8, data=b'\x00' * 8, sequence = 0)"
					python3 send_scapy.py --direction outbound "IP()/UDP(dport = 10000, sport = 123)/NTPControl(response=1, status_word=NTPSystemStatusPacket(), op_code = 1, count = 8, data= b'\x00' * 8, more = 1, offset = 0)"
					python3 send_scapy.py --direction outbound "IP()/UDP(dport = 10000, sport = 123)/NTPControl(response=1, status_word=NTPSystemStatusPacket(), op_code = 1, count = 8, data= b'\x00' * 8, more = 1, offset = 8)"
					python3 send_scapy.py --direction outbound "IP()/UDP(dport = 10000, sport = 123)/NTPControl(response=1, status_word=NTPSystemStatusPacket(), op_code = 1, count = 8, data= b'\x00' * 8, more = 1, offset = 16)"
					python3 send_scapy.py --direction outbound "IP()/UDP(dport = 10000, sport = 123)/NTPControl(response=1, status_word=NTPSystemStatusPacket(), op_code = 1, count = 8, data= b'\x00' * 8, more = 0, offset = 24)"
					;;										
			esac
		fi
	;;		

	
esac


