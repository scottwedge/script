#/bin/bash

pcapname=/home/pcap/ntp/ntp_private.pcap
yamldir=/home/tmp/module/ntp/

if [ -z "$1" ]
then
	#private retran
	python3 replay_test.py --yaml ${yamldir}private_trans_error.yml --pcap $pcapname 


	#private Unsolicited Response
	python3 replay_test.py --yaml ${yamldir}private_unsolicited_error.yml --pcap $pcapname 


	#private Reflection Deny	
	python3 send_scapy.py "IP()/UDP()/NTPPrivate(mode=7)"


    #private sequence do not match error

	#resposne reply 3 packet,the last is droped;
    python3 replay_test.py --yaml ${yamldir}private_sequence_error_mul.yml --pcap $pcapname 
	
	#resposne reply 1 packet is droped;
    python3 replay_test.py --yaml ${yamldir}private_sequence_error_single.yml --pcap $pcapname 
	
	#resposne reply 2 packet ,the last is droped;
    python3 replay_test.py --yaml ${yamldir}private_sequence_more_error.yml --pcap $pcapname 


    #private version error

	#client send 3 packets,all drop
    python3 replay_test.py --yaml ${yamldir}private_version_error.yml --pcap $pcapname 


	#private request len error
    
	#private len < 8
	python3 send_scapy.py "IP(options=[IPOption_RR(routers=['1.1.1.1'] * 6)])/UDP(sport = 123, dport=123)/Raw(b'\x17\x00\x03\x00\x00\x00\x00')"

    #private len > 216
    python3 send_scapy.py "IP()/UDP()/NTPPrivate(mode=7)/Raw(b'\x00' * 209)"
	
	#private itemsize * itemcount > length(ntpraw)
	python3 send_scapy.py "IP()/UDP()/NTPPrivate(mode=7, nb_items = 4, data_item_size=17)/Raw((b'\x00' * 64))"


	#private response len error
    
	#private len < 8
	python3 send_scapy.py --direction outbound "IP(options=[IPOption_RR(routers=['1.1.1.1'] * 6)])/UDP(sport = 123, dport=123)/Raw(b'\x97\x00\x03\x00\x00\x00\x00')"

    #private len > 508 
    python3 send_scapy.py --direction outbound "IP()/UDP()/NTPPrivate(response = 1, mode=7)/Raw(b'\x00' * 501)"
	
	#private itemsize * itemcount > length(ntpraw)
	python3 send_scapy.py --direction outbound "IP()/UDP()/NTPPrivate(mode=7, nb_items = 4, data_item_size=17, response = 1)/Raw(b'\x00' * 64)"
else

	#private retran
	python3 replay_test.py --yaml ${yamldir}private_trans_pass.yml --pcap $pcapname 

    #private seq match 
    python3 replay_test.py --yaml ${yamldir}private_sequence_pass_mul.yml --pcap $pcapname 
    python3 replay_test.py --yaml ${yamldir}private_sequence_pass_single.yml --pcap $pcapname


    #private version  

	#client send 3 packets,all forward 
    python3 replay_test.py --yaml ${yamldir}private_version_pass.yml --pcap $pcapname 

	#private request len

    #private len < 216
    python3 send_scapy.py "IP()/UDP()/NTPPrivate(mode=7)/Raw(('\x00' * 208))"

    #private len > 8 
    python3 send_scapy.py "IP(options=[IPOption_RR(routers=['1.1.1.1'] * 6)])/UDP()/NTPPrivate(mode=7)/Raw(b'\x00' * 0)"

	#private itemsize * itemcount <= length(ntpraw)
	python3 send_scapy.py "IP()/UDP()/NTPPrivate(mode=7, nb_items = 4, data_item_size=15)/Raw(b'\x00' * 64)"
	python3 send_scapy.py "IP()/UDP()/NTPPrivate(mode=7, nb_items = 4, data_item_size=16)/Raw(b'\x00' * 64)"


	#private response len

    #private len < 216
    python3 send_scapy.py --direction outbound "IP()/UDP()/NTPPrivate(mode=7, response = 1)/Raw(b'\x00' * 500)"

    #private len > 8 
    python3 send_scapy.py --direction outbound "IP(options=[IPOption_RR(routers=['1.1.1.1'] * 6)])/UDP()/NTPPrivate(response = 1, mode=7)/Raw(b'\x00' * 0)"

	#private itemsize * itemcount <= length(ntpraw)
	python3 send_scapy.py --direction outbound "IP()/UDP()/NTPPrivate(mode=7, nb_items = 4, data_item_size=15, response = 1)/Raw(b'\x00' * 64)"
	python3 send_scapy.py --direction outbound "IP()/UDP()/NTPPrivate(mode=7, nb_items = 4, data_item_size=16, response = 1)/Raw(b'\x00' * 64)"
fi

