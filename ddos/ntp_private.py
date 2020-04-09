#!/bin/python
import getopt
import sys
from ddosMain import *


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("""
            para1:    0 client, 1 server.
            para2:  
                      1 Version Anomaly            para3:version.(2-4 forward, 0-1 or > 4 block.)
                      2 Retransmission.            para3:NONE
                      3 Sequence Mismatch          para3:sequence

            """)
        sys.exit(1)
    address = os.environ.get('tdip')
    port = os.environ.get("tport")
    pcap = "/home/pcap/ntp/ntp_private.pcap"
    #pcap = "/home/yangzhengchu/fortinet/ddos/pcap/ntp_custom/ntp_private.pcap"
    pkts = rdpcap(pcap)
    if int(sys.argv[1]) == 0:
        pkt = pkts[0]
    else:
        pkt = pkts[1]

    ob = ddos_send(port, address)

    opt = int(sys.argv[2])


    if opt == 1:
        ntpdict = {}
        version = int(sys.argv[3])
        ntpdict["version"] = version 
    if opt == 2:
        ntpdict = {}
        ob.relay_private_pcap_by_scapy(pkt, ntpdict)
    if opt == 3:
        ntpdict = {}
        value = int(sys.argv[3])
        ntpdict["seq"] = value         

    ob.relay_private_pcap_by_scapy(pkt, ntpdict)
