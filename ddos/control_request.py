from scapy.all import *
import sys

code =sys.argv[1]

src = "127.0.0.1"
dst = "127.0.0.2"
pkt = IP(src=src,dst=dst,len=40)/UDP(len=20)/NTPControl(op_code = int(code), association_id = 29519)/"\0\0\0\0\0"
send(pkt)

