#!/usr/bin/python3
import sys
from scapy.all import *


src = "1.0.0.1"
dst = "1.0.0.2"
data = "a" * 18


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("""

		1 - IP version other than 4 or  
		2 - Header length less than 5 words     ---      IP hearder length 字段小于5.
		3 ? End of packet (EOP) before 20 bytes of IPV4 Data    ---
		4 - Total length less than 20 bytes     ---      IP total length 字段小于20.
		5 - EOP comes before the length specified by Total length 　---  　 IP包实际size小于ip total length字段指定大小
		6 - End of Header before the data offset (while parsing options)  --- option len field + 20(ip basic)> header len field;
		7 - Length field in LSRR/SSRR option is other than (3+(n*4)) where n takes value greater than or equal to 1
		8 - Pointer in LSRR/SSRR is other than (n*4) where n takes value greater than or equal to 1
		?9 - For IP Options length less than 3
		10 - Reserved flag set    para 1:reverse flag(1 or 0)
		11 - More fragments flag set incorrectly
		12 - header length field is bigger than real size of packet's ip part.
		""")
        sys.exit(0)
    option = int(sys.argv[1])
    if option == 1:
        send(IP(src=src, dst = dst, version=5)/UDP()/data)
    if option == 2:
        send(IP(src=src, dst = dst, ihl=4)/UDP()/data)
    if option == 4:
        value = int(sys.argv[2]) if len(sys.argv) > 2 else 19
        send(IP(src=src, dst = dst, len = value)/UDP(sport= 1024, dport = 1024))
    if option == 5:
        if len(sys.argv) > 2:
            value = int(sys.argv[2])
        else:
            value = 54 
        send(IP(src = src, dst = dst, len=value)/UDP(sport=1024, dport=1024)/('a' * 22))
    if option == 6:#header len field 36(9) - 20 = 16.option field 15,16 forward, > 16 block. 
        if len(sys.argv) > 2:
            value = int(sys.argv[2])
        else:
            value = 17 
        send(IP(src=src, dst=dst, 
               options=[IPOption_RR(routers=['1.1.1.1'] * 3, 
			 					  pointer=4, 
								  length = value)]
							     )/UDP(sport=1024, dport=1024)) 
    if option == 7: #长度字段应该是3 * n + 3 and n > 0.  block: 3 8 12 13  forward 7 11 15
        if len(sys.argv) > 2:
            len = int(sys.argv[2])
        else:
            len = 16 
        pkt = IP(src=src, dst=dst, 
        options=[IPOption_LSRR(routers=['1.1.1.1'] * 3, length = len)])/UDP(sport=1024, dport=1024)
        send(pkt)

    if option == 8: #pointer字段需是n * 4 and n > 0, block 0 7 13 forward 4 8 16
        if len(sys.argv) > 2:
            point = int(sys.argv[2])
        else:
            point = 5
        pkt = IP(src=src, dst=dst, 
        options=[IPOption_LSRR(routers=['1.1.1.1'] * 3, pointer=point)])/UDP(sport=1024, dport=1024)
        send(pkt)

    if option == 10:
        if len(sys.argv) > 2:
            flag = int(sys.argv[2])
        else:
            flag = 1
        pkt = IP(src = src, dst = dst)/UDP(sport=1024, dport=1024)
        pkt.flags.evil = flag 
        send(pkt)

    if option == 11:
        if len(sys.argv) > 3:
            mf = bool(int(sys.argv[2]))
            df = bool(int(sys.argv[3]))
            print(mf, df)
        else:
            mf = 1 
            df = 1 
        pkt = IP(src = src, dst = dst)/UDP(sport=1024, dport=1024)
        pkt.flags.MF = mf
        pkt.flags.DF = df 
        send(pkt)

    if option == 12:# 7 * 4 + 3 + 20 + 1(option padding)= 52, block 14 * 4, allow 13 * 4
        if len(sys.argv) > 2:
            value = int(sys.argv[2])
        else:
            value = 14
        pkt = IP(src = src, dst = dst, ihl = value ,len = value * 4, options = [IPOption_RR(routers = ["1.1.1.1"] * 7)])
        send(pkt)

