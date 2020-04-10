import netifaces
from scapy.all import *
import argparse
import time

class tool(object):
    def get_ip_mac(port):
        ip = netifaces.ifaddresses(port)[netifaces.AF_INET][0]['addr']
        mac = netifaces.ifaddresses(port)[netifaces.AF_LINK][0]['addr']
        return (mac, ip)

    def parse_yaml(template, variable_dict = {}):
        fp = open(template, 'r')
        data = fp.read()
        fp.close()
        template = Template(data)
        data_handle = template.render(**variable_dict)
        result = yaml.load(data_handle, Loader = yaml.FullLoader)
        return result 

def get_info_by_direction(direction):
    d = {}
    if direction == "inbound":
        d["siface"] = "eth1"
        d["riface"] = "eth2"
    else:
        d["siface"] = "eth2"
        d["riface"] = "eth1"

    d['src']= tool.get_ip_mac(d["siface"])
    d['dst']= tool.get_ip_mac(d["riface"])
    return d

def send_scapy_command(command, direction, option):
    d = get_info_by_direction(direction)
    pkt = Ether()/eval(command)
    pkt[Ether].src = d["src"][0]
    pkt[Ether].dst = d["dst"][0]

    if pkt[IP].src == "127.0.0.1":
        pkt[IP].src = d["src"][1]
    if pkt[IP].dst == "127.0.0.1":  
        pkt[IP].dst = d["dst"][1]
    t = AsyncSniffer(iface = d["riface"])
    t.start()
    time.sleep(0.1)    
    sendp(pkt, iface = d["siface"])
    res = t.stop()
    if option.get("verbose"):
        for i in res:
            print(i.show2())
    else:
        print(res.nsummary())

def usage():
    parser = argparse.ArgumentParser(description='replay pcap')
    parser.add_argument('--yaml', help ="yaml file")
    parser.add_argument('--direction', default = "inbound",help ="direction info")
    parser.add_argument('-v', '--verbose', help ="display recieve detail", action="store_true")    
    parser.add_argument('command', help='scapy command')
    args = parser.parse_args()
    return args

if __name__ == "__main__":
    args = usage()
    option = {"verbose": args.verbose}
    send_scapy_command(args.command, args.direction, option)
