import sys
import os
from scapy.all import *
import get_info

"""
1. stric icmp abnormal check.
"""

class icmp_packet:
    def __init__(self, src, dst, smac, port):
        self.src = src
        self.dst = dst
        self.smac = smac
        self.port = port

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

    def send_ntp_version(self, num):
        p = IP(src = self.src, dst = self.dst)/UDP()/NTP()
        p[NTP].version = num
        sr(p, inter=0.1, timeout = 0.5)

    def reply_ntp_version(self, version, mode = 4):
        pkts = sniff(iface=self.port, count = 1,filter="udp and dst port 123 and ip src %s"%self.dst)
        pkt = pkts[0]
        if pkt[NTP].mode == 3:
            p = IP()/UDP()/NTP(mode = 4)
            p.src = pkt[IP].dst
            p.dst = pkt[IP].src
            p[NTP].version = version
            p[NTP].mode = mode
            send(p)

    def relay_pcap_by_scapy(self, pcap):
        pkts = rdpcap(pcap)
        for pkt in pkts:
            pkt = pkts[0]
            pkt[IP].dst = self.dst
            pkt[IP].src = self.src 
            #pkt[Ether].src = self.smac
            del pkt[IP].chksum
            del pkt[Ether].src
            del pkt[Ether].dst
            sendp(pkt, iface=self.port)

if __name__ == '__main__':
    dip = sys.argv[1]
    port = sys.argv[2] if len(sys.argv) > 2 else "eth1"

   
    smac, sip = get_info.get_mac_and_ip(port)
    ob = icmp_packet(sip, dip, smac, port)
    d = "/home/yangzhengchu/fortinet/ddos/pcap/"
    ob.relay_pcap_by_scapy(d + sys.argv[3])
    #ob.send_icmp_bad_checksum()
    #ob.send_ip_bad_checksum()

