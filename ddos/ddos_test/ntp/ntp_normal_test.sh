#/bin/bash

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
				1)#mode field should be zero when version = 1,mode not zero 
					./scapy_test.py ntp_normal_version_block1.yml
					;;
				2)#version should be 1-4, error version 0,5 
					./scapy_test.py ntp_normal_version_block2.yml
					;;
			esac
		else
			case "$index" in
				1)#mode field should be zero when version = 1,mode zero and other version not zero. 
                    ./scapy_test.py ntp_normal_version_forward1.yml
					;;
				2)#version should be 1-4, test 1-4 
					./scapy_test.py ntp_normal_version_forward2.yml
					;;
			esac
		fi
	;;		
	stratum)
		if [ "$action" = "block" ]
		then
			case "$index" in
				1)# Normal Stratum Anomaly Check,stratum should be in 1 < stratum < 15 ,test 16, 255
					./scapy_test.py ntp_normal_stratum_block1.yml
					;;
				2)# Normal Stratum Anomaly Check,referince id should be not NULL when stratum > 1.test stratum 2 8 15 and ref id == NULL 
					./scapy_test.py ntp_normal_stratum_block2.yml
					;;
			esac
		else
			case "$index" in
				1)# Normal Stratum Anomaly Check,stratum should be in 1 < stratum < 15 ,test 0 8 15
					./scapy_test.py ntp_normal_stratum_forward1.yml
					;;
				2)# Normal Stratum Anomaly Check,referince id should be not NULL when stratum > 1. test stratum 2 8 15 and ref id == NULL and 0,1 ref == NULL 
					./scapy_test.py ntp_normal_stratum_forward2.yml
					;;
			esac
		fi
	;;		
	len)
		if [ "$action" = "block" ]
		then
			case "$index" in
				1) # version 1, 2, 3, 4len < 48
					python3 send_scapy.py "IP()/UDP(sport=123,dport=123)/Raw(raw(NTP(version = 1, mode = 0))[:-1])"
					python3 send_scapy.py "IP()/UDP(sport=123,dport=123)/Raw(raw(NTP(version = 2))[:-1])"
					python3 send_scapy.py "IP()/UDP(sport=123,dport=123)/Raw(raw(NTP(version = 3))[:-1])"
					python3 send_scapy.py "IP()/UDP(sport=123,dport=123)/Raw(raw(NTP(version = 4))[:-1])"	
					python3 /tmp/script/tmp.py  s2 | grep ntp				
					;;
				2) # version 1 > 48
					python3 send_scapy.py "IP()/UDP()/NTP(version = 1, mode = 0)/Raw(b'\x00' * 12)"
					python3 send_scapy.py "IP()/UDP()/NTP(version = 1, mode = 0)/Raw(b'\x00' * 4)"
					python3 send_scapy.py "IP()/UDP()/NTP(version = 1, mode = 0)/Raw(b'\x00' * 1)"
					python3 /tmp/script/tmp.py  s2 | grep ntp
					
					;;		
				3) # version 2/3 48 or 60    56,64,61
					python3 send_scapy.py "IP()/UDP()/NTP(version = (2,3))/Raw(b'\x00' * 8)"
					python3 send_scapy.py "IP()/UDP()/NTP(version = (2,3))/Raw(b'\x00' * 13)"
					python3 send_scapy.py "IP()/UDP()/NTP(version = (2,3))/Raw(b'\x00' * 16)"		
					python3 /tmp/script/tmp.py  s2 | grep ntp		
					;;
				4) #when  0 < len - 48 < 24,have data no option,len -48 %4 should be 0.
					python3 send_scapy.py "IP()/UDP()/NTP(version = 4)/Raw(b'\x00' * 3)"
					python3 send_scapy.py "IP()/UDP()/NTP(version = 4)/Raw(b'\x00' * 22)"	
					python3 /tmp/script/tmp.py  s2 | grep ntp			
					;;				
				5) # > 24,have extension ,all extesion length field %4 != 0
				    python3 send_scapy.py "IP()/UDP()/NTP()/NTPExtension(type=1, len=35,value=b'\x01' * 30)"
				    python3 send_scapy.py "IP()/UDP()/NTP()/NTPExtension(type=1, len=36,value=b'\x01' * 30)/NTPExtension(type=1, len=35,value=b'\x01' * 30)"
				    python3 /tmp/script/tmp.py  s2 | grep ntp
				    ;;
				6) # > 24,have extension ,sum all extesion length field + 48 > ntp len 
				    python3 send_scapy.py "IP()/UDP()/NTP()/NTPExtension(type=1, len=36,value=b'\x01' * 30)/NTPExtension(type=1, len=37,value=b'\x01' * 30)"
				    python3 send_scapy.py "IP()/UDP()/NTP()/NTPExtension(type=1, len=36,value=b'\x01' * 30)/NTPExtension(type=1, len=40,value=b'\x01' * 30)"
				    python3 /tmp/script/tmp.py  s2 | grep ntp
				    ;;				    
			esac
		else
			case "$index" in
				1) # ntp len =48
					python3 send_scapy.py "IP()/UDP()/NTP(version = 1, mode = 0)"
					python3 send_scapy.py "IP()/UDP()/NTP(version = (2,4))"
					python3 send_scapy.py "IP()/UDP()/NTP(version = [2,3])/Raw(b'\x00' * 12)"
					python3 /tmp/script/tmp.py  s2 | grep ntp
					;;
				4) # when 0 < len - 48 < 24,have data no option,len -48 %4 should be 0.
					python3 send_scapy.py "IP()/UDP()/NTP(version = 4)/Raw(b'\x00' * 4)"
					python3 send_scapy.py "IP()/UDP()/NTP(version = 4)/Raw(b'\x00' * 20)"
					python3 send_scapy.py "IP()/UDP()/NTP(version = 4)/Raw(b'\x00' * 24)"	
					;;		
				5) #  > 24,have extension ,all extesion length field %4 == 0
				    python3 send_scapy.py "IP()/UDP()/NTP()/NTPExtension(type=1, len=36,value=b'\x01' * 30)"
				    python3 send_scapy.py "IP()/UDP()/NTP()/NTPExtension(type=1, len=36,value=b'\x01' * 30)/NTPExtension(type=1, len=36,value=b'\x01' * 30)"
					python3 /tmp/script/tmp.py  s2 | grep ntp
					;;	
				6) #  > 24,have extension ,sum all extesion length field + 48 <= ntp len 
					# equal
				    python3 send_scapy.py "IP()/UDP()/NTP()/NTPExtension(type=1, len=36,value=b'\x01' * 30)/NTPExtension(type=1, len=36,value=b'\x01' * 30)"
				    #smaller
				    python3 send_scapy.py "IP()/UDP()/NTP()/NTPExtension(type=1, len=36,value=b'\x01' * 30)/NTPExtension(type=1, len=32,value=b'\x01' * 30)"
					python3 /tmp/script/tmp.py  s2 | grep ntp
					;;															
			esac			
		fi
	;;		
	trans)
		if [ "$action" = "block" ]
		then
			case "$index" in
				1)#mode 1,3,5 retren check 
					./scapy_test.py ntp_normal_retran_block1.yml
					;;
				2)#mode 1,3 retran timeout check
					./scapy_test.py ntp_normal_retran_block2.yml
					;;
				3)#mode 5 retran timeout check
					./scapy_test.py ntp_normal_retran_block3.yml
					;;
				4)#mode 1,3 do not retran after reply check
					./scapy_test.py ntp_normal_retran_block4.yml
					;;
			esac
		fi		
	;;
	unsol)
		if [ "$action" = "block" ]
		then
			case "$index" in
				1) 
				./scapy_test.py ntp_normal_unsol_block.yml
				   	;;
			esac
		fi		
	;;				
	mode)
		if [ "$action" = "block" ]
		then
			case "$index" in
				1) # mode control enable/disable test
					./scapy_test.py ntp_normal_mode_block.yml
					;;
				b) # all mode pair loop
					
					;;					
			esac
		else
			case "$index" in
				1) # all correct pair
					./scapy_test.py ntp_normal_mode_forward.yml
					;;
			esac			
		fi
	;;		
esac


