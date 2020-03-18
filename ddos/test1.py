from ip_abnormal import *

dip = sys.argv[1]
port = sys.argv[2] if len(sys.argv) > 2 else "eth1"


smac, sip = get_info.get_mac_and_ip(port)
ob = icmp_packet(sip, dip, smac, port)
d = "/home/yangzhengchu/fortinet/ddos/pcap/"
ob.send_ntp_version(4)



