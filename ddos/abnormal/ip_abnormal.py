import sys
import os
from scapy.all import *
"""
1. stric icmp abnormal check.
"""

class icmp_packet:
    def __init__(self, src, dst):
        self.src = src
        self.dst = dst
    def send_icmp_less_field(self):
        """
        1. send icmp packet with 7 bytes(8 less normal).
        """
        rawinfo = raw(IP(dst=self.dst, src=self.src)/ICMP())[0:-2]
        pkt = IP(rawinfo)
        del pkt.len
        del pkt.chksum
        rep = send(pkt)
    def send_icmp_bad_checksum(self):
        os.popen("hping3 -1 %s -c 1 -b"%self.dst)

    def send_ip_bad_checksum(self):
        pkt = IP(src = self.src, dst = self.dst)/ICMP()
        pkt["IP"].chksum = 0x1111
        send(pkt)

if __name__ == '__main__':
    src = "172.22.101.138"
    dst = sys.argv[1]
    ob = icmp_packet(src, dst)
    ob.send_icmp_less_field()
    ob.send_icmp_bad_checksum()
    ob.send_ip_bad_checksum()
