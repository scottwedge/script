import sys
import os
import re
from scapy.all import *

"""
1. stric icmp abnormal check.
"""

class ddos_send(object):
    def __init__(self, port, dst, sip = None):

        self.port = port
        self.dst = dst
        self.smac, self.src = self.get_mac_and_ip(self.port)
        if sip:
            self.src = sip

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


if __name__ == '__main__':
    dip = sys.argv[1]
    port = sys.argv[2] if len(sys.argv) > 2 else "eth1"


    ob = ddos_send(port, dip)
    d = "/home/yangzhengchu/fortinet/ddos/pcap/"
    ob.relay_pcap_by_scapy(d + sys.argv[3])

