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

    def get_mac_and_ip(self, port):
        if port == "lo":
            mac, ip = "00:00:00:00:00:00", "127.0.0.1"
        else:
            fb = os.popen("ip addr show %s" %port)
            data = fb.read()
            pattern = re.compile(r'ether ((?:(?:[0-9a-f]{2}[:]){5})[0-9a-f]{2}).*inet ((?:(?:[0-9]{1,3}\.){3}[0-9]{1,3}))/', re.IGNORECASE|re.S)
            infos = pattern.search(data).groups()
            if len(infos) == 2:
                mac, ip = infos
        return mac, ip 

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
        res = sr1(p, inter=0.1, timeout = 0.5)
        #if res:
            #print(res[NTP].show2())
        return res

    def get_ntp_header(self):
        print(NTP().show2()) 

    def send_ntp_packet(self, data):
        p = IP(src = self.src, dst = self.dst)/UDP()/NTP(**data)
        res = sr1(p, inter=0.1, timeout = 0.5)
        return res
    
    def reply_ntp_packet(self, data):
        pkts = sniff(iface=self.port, count = 1,filter="udp and dst port 123 and ip src %s"%self.dst)
        pkt = pkts[0]
        if pkt:
            data.setdefault("mode", 4);
            p = IP()/UDP()/NTP(**data)
            p.src = pkt[IP].dst
            p.dst = pkt[IP].src
            send(p)
        return pkt 

    def relay_pcap_by_scapy(self, pcap):
        pkts = rdpcap(pcap)
        for pkt in pkts:
            #pkt = pkts[0]
            pkt[IP].dst = self.dst
            pkt[IP].src = self.src 
            #pkt[Ether].src = self.smac
            del pkt[IP].chksum
            del pkt[Ether].src
            del pkt[Ether].dst
            sendp(pkt, iface=self.port)

    def relay_control_pcap_by_scapy(self, pcap, ntpdict):
        pkts = rdpcap(pcap)
            
        for pkt in pkts:
            if ntpdict == None:
                print(pkt[NTPControl].show2())
                continue
            #pkt = pkts[0]
            for key, value in ntpdict.items():
                setattr(pkt[NTPControl], key, value)
            del pkt[UDP].len
            pkt[IP].dst = self.dst
            pkt[IP].src = self.src
            #pkt[Ether].src = self.smac
            del pkt[IP].chksum
            del pkt[IP].len
            del pkt[Ether].src
            del pkt[Ether].dst
            sendp(pkt, iface=self.port)

    def relay_private_pcap_by_scapy(self, pkt, ntpdict):
        if ntpdict == None:
            print(pkt[NTPPrivate].show2())

        else:
            for key, value in ntpdict.items():
                setattr(pkt[NTPPrivate], key, value)
            del pkt[UDP].len
            pkt[IP].dst = self.dst
            pkt[IP].src = self.src
            #pkt[Ether].src = self.smac
            del pkt[IP].chksum
            del pkt[IP].len
            del pkt[Ether].src
            del pkt[Ether].dst
            sendp(pkt, iface=self.port)


if __name__ == '__main__':
    dip = sys.argv[1]
    port = sys.argv[2] if len(sys.argv) > 2 else "eth1"


    ob = ddos_send(port, dip)
    d = "/home/yangzhengchu/fortinet/ddos/pcap/"
    ob.relay_pcap_by_scapy(d + sys.argv[3])
    #ob.send_icmp_bad_checksum()
    #ob.send_ip_bad_checksum()

