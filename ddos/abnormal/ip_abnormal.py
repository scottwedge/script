import sys
import os
from scapy.all import *
import get_info

"""
1. stric icmp abnormal check.
"""

class icmp_packet:
    def __init__(self, src, dst, smac):
        self.src = src
        self.dst = dst
        self.smac = smac

    def send_icmp_less_field(self):
        """
        1. send icmp packet with 7 bytes(8 less normal).
        """
        rawinfo = raw(IP(dst=self.dst, src=self.src,options=[IPOption('%s%s'%('\x86\x28','a'*21))])/ICMP())[0:-2]
        pkt = IP(rawinfo)
        pkt.psend()
        del pkt.len
        del pkt.chksum
        rep = send(pkt)
    def send_icmp_bad_checksum(self):
        os.popen("hping3 -1 %s -c 1 -b"%self.dst)

    def send_ip_bad_checksum(self):
        pkt = IP(src = self.src, dst = self.dst)/ICMP()
        pkt["IP"].chksum = 0x1111
        send(pkt)
    def test(self):
        pkts = rdpcap("../icmp_malformed_abnormal_bak.pcap")
        pkt = pkts[0]
        pkt[IP].dst = self.dst
        pkt[IP].src = self.src 
        #pkt[Ether].src = self.smac
        del pkt[IP].chksum
        del pkt[Ether].src
        del pkt[Ether].dst
        sendp(pkt, iface="wlp9s0")

if __name__ == '__main__':
    src = "10.10.10.152"
    if len(sys.argv) == 3:
       port = sys.argv[2] 
    else:
        port = "eth1"

    smac, src = get_info.get_mac_and_ip(port)
    ob = icmp_packet(src, sys.argv[1], smac)
    ob.test()
    #ob.send_icmp_bad_checksum()
    #ob.send_ip_bad_checksum()
