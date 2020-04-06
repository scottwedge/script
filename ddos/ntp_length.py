from scapy.all import *
import sys
src, dst = "127.0.0.1" , "127.0.0.2"
#src, dst = "11.1.1.2" , "11.1.2.2"

args = sys.argv[1::]

if __name__ == "__main__":

    if len(args) == 0:
        print("""
        para1 mode
        para2 version
        para3 length
        """)
        sys.exit(0)
    else:
        nfield = raw(NTP(mode = int(args[0]), version = int(args[1])))
        length = int(args[2])
        if length < 0:
            data = nfield[0:length]
        else:
            data = nfield + b"a" * length

    print("len %d"%length)

    send(IP(src=src, dst=dst)/UDP(sport=123, dport=123)/data)





