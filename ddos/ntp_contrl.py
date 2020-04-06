#!/bin/python
import getopt
import sys
from ddosMain import *


if __name__ == '__main__':
    address = os.environ.get('tdip')
    port = os.environ.get("tport")
    #pcap = "/home/pcap/ntp/ntp_control_respose_one.pcap"
    pcap = "/home/yangzhengchu/fortinet/ddos/pcap/ntp_custom/ntp_control_respose_one.pcap"

    ob = ddos_send(port, address)
    if(len(sys.argv) < 2):
        ob.relay_control_pcap_by_scapy(pcap, None) 
        sys.exit(0) 

    opt = sys.argv[1]

    pkts = []
    if int(opt) == 1:#Response with COUNT value as 0
        d = {}
        para = sys.argv[2]
        length = int(para)
        data = b'' if length == 0 else b'a' * length
        print(data)
        d["data"] = data 
        d["count"] = len(data) 
        pkts.append(d)
    elif int(opt) == 2:#Fragmented error response(E=1 and M=1)
        d = {}
        para1 = int(sys.argv[2])                
        para2 = int(sys.argv[3])                
        d["err"] = para1
        d["more"] = para2
        pkts.append(d)
    elif int(opt) == 31:
        d1 = {}
        data = 'a' * 468 
        d1["data"] = data 
        d1["count"] = 468
        d1["more"] = 1 
        pkts.append(d1)

        d2 = {}
        d2["data"] = data 
        d2["count"] = 468
        d2["more"] = 1 
        d2["offset"] = 468
        pkts.append(d2)

        d3 = {}
        d3["data"] = 'a' * 100
        d3["count"] = 100 
        d3["offset"] = 468 + 468
        pkts.append(d3)

    elif int(opt) == 32:#First response with M=1 with non-zero OFFSET
        d1 = {}
        data = 'a' * 468 
        d1["data"] = data 
        d1["count"] = 468
        d1["more"] = int(sys.argv[2])
        d1["offset"] = int(sys.argv[3]);
        pkts.append(d1)
    
    if int(opt) == 4:#Response with COUNT > Length of data
        d = {}
        para2 = int(sys.argv[2])
        length = int(sys.argv[3])
        data = 'a' * length
        d["data"] = data 
        d["count"] = para2
        pkts.append(d)
 
    if int(opt) == 5:#Response with reserved STATUS values( >7)
        d = {}
        para = sys.argv[3]
        length = int(para)
        data = b'' if length == 0 else b'a' * length
        d["err"] = 1 
        d["count"] = len(data)
        d["data"] = data
        
        s = NTPErrorStatusPacket()
        s.error_code = int(sys.argv[2])
        d["status_word"] = s

        pkts.append(d)

    if int(opt) == 6:#sequence mismatch
        d = {}
        para = int(sys.argv[2])
        d["sequence"] = para
        pkts.append(d)


            
    for pkt in pkts:
        ob.relay_control_pcap_by_scapy(pcap, pkt)

