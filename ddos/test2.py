from ip_abnormal import *

dip = sys.argv[1]
port = sys.argv[2] if len(sys.argv) > 2 else "eth1"

smac, sip = get_info.get_mac_and_ip(port)
ob = ddos_send(sip, dip, smac, port)
pkt = ob.reply_ntp_version(2, 4)
if pkt:
    print(pkt[NTP].show2());




