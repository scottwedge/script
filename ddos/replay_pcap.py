import netifaces
from scapy.all import *
import argparse
import sys
from pprint import pprint
import traceback
import time
"""
    [
        {   direction
            protocol: tcp
            "id":1,
            "pcap_data":
                { 
                    NTPPrivate:
                    {
                        "update_data":
                            {
                                "key": value,
                            }
                        "rest_data":[chksum]
                            ""
                    }
               } 
            "send_data":
                {
                    "iface": "eth1",
                    "sleep": 1,
                    "verbose":0,
                }
        }
    ]
"""



parser = argparse.ArgumentParser(description='replay pcap')
parser.add_argument('pcap', help ="replay pcap")
parser.add_argument('-y', help ="yaml file")
parser.add_argument('-d', help ="data info")


class tool(object):
    def get_ip_mac(port):
        ip = netifaces.ifaddresses(port)[netifaces.AF_INET][0]['addr']
        mac = netifaces.ifaddresses(port)[netifaces.AF_LINK][0]['addr']
        return (mac, ip)


class generate_data(object):
    def __init__(self, data):
        self.data = data
        self.layer4 = self.data.get("protocol", "");
        direction = self.data.get("direction", "inbound")
        if direction == "inbound":
            self.siface = "eth1"
            self.riface= "eth2"
        else:
            self.siface = "eth2"
            self.riface = "eth1"

        self.src= tool.get_ip_mac(self.siface)
        self.dst= tool.get_ip_mac(self.riface)

    
    
    def generate_default(self):
        self.layer2_data = {
                "update_data": {
                    "src": self.src[0], 
                    "dst": self.dst[0], 
                },
                "rest_data":[
                ]
        }

        self.layer3_data = {
                "update_data": {
                    "src": self.src[1], 
                    "dst": self.dst[1], 
                },
                "rest_data":[
                    "chksum",
                    "len"
                ]
        }


        if self.layer4 == "UDP":
            rest_data = ["len"]
        elif self.layer4 == "TCP":
            rest_data = ["chksum"]
        else:
            rest_data = []

        rest_dat = []
        self.layer4_data = {
                "update_data": {
                },
                "rest_data": rest_data
        }


    def make_data(self):
        self.generate_default()
        d = {}
        d["id"] = self.data["id"]

        d["send_data"] = {
                "iface": self.siface,
                "sleep": 0,
                "verbose": 0,
                }
        d["send_data"].update(self.data.get("send_data", {}))

        orig_data = self.data.get("pcap_data", {})
        if "Ether" in orig_data:
            self.layer2_data["update_data"].update(orig_data["Ether"].get("update_data", {}))
            orig_data["Ether"]["update_data"] = self.layer2_data["update_data"]
            orig_data["Ether"]["rest_data"] = set(self.layer2_data["rest_data"] + (orig_data["Ether"].get("rest_data", [])))
        else:
            orig_data["Ether"] = self.layer2_data
        
        if "IP" in orig_data:
            self.layer3_data["update_data"].update(orig_data["IP"].get("update_data", {}))
            orig_data["IP"]["update_data"] = self.layer3_data["update_data"]
            orig_data["IP"]["rest_data"] = set(self.layer3_data["rest_data"] + (orig_data["IP"].get("rest_data", [])))
        else:
            orig_data["IP"] = self.layer3_data

        if self.layer4 in ['TCP', 'UDP']:
            if self.layer4 in orig_data:
                self.layer4_data["update_data"].update(orig_data[self.layer4].get("update_data", {}))
                orig_data[self.layer4]["update_data"] = self.layer4_data["update_data"]
                orig_data[self.layer4]["rest_data"] = set(self.layer4_data["rest_data"] + (orig_data[self.layer4].get("rest_data", [])))
            else:
                orig_data[self.layer4] = self.layer4_data
        d["pcap_data"] = orig_data
        return d


class handle_pcap(object):
    def __init__(self, pcap):
        self.pcap = pcap
        self.pkts = rdpcap(self.pcap)

    def relay_private_pcap_by_scapy(self, pcaplist):
        try:
            for pcap_info in pcaplist:
                pcap_id = pcap_info.get("id")
                pcap_data = pcap_info.get("pcap_data")
                send_data = pcap_info.get("send_data")
                pkt = self.pkts[pcap_id]
                self.update_pcap(pkt, pcap_data)
                self.send_pcap(pkt, send_data)

        except Exception as e:
            print("function relay_private_pcap_by_scapy error %d %s"%(pcap_id, str(e)))
            traceback.print_exc()


    def update_pcap(self, pkt, pkt_data):
        try:
            for level_obj, data in pkt_data.items():
                level_obj = eval(level_obj)
                update_data = data.get("update_data", {})
                reset_data = data.get("rest_data", [])
                for key, value in update_data.items():
                    setattr(pkt[level_obj], key, value)
                 
                for key in reset_data: 
                    if key not in update_data:
                        delattr(pkt[level_obj], key)
        except Exception as e:
            print("update pcap error %s" %str(e))
            traceback.print_exc()

    def send_pcap(self, pkt, send_info):
        iface = send_info.get("iface")
        sleep_time = send_info.get("sleep")
        verbose= send_info.get("verbose")
        if sleep_time:
            time.sleep(sleep_time)
        if verbose:
            print(pkt.show2())        
        sendp(pkt, iface = iface)




if __name__ == "__main__":
    print("hello")
    a = [
            {
                # "direction": "inbound",
                # "protocol": "UDP", 
                "id":0,
                "pcap_data":
                    { 
                        "NTPPrivate":
                        {
                            "update_data":
                                {
                                    "version": 4,
                                }
                        },
                        # "IP":
                        # {
                        #     "update_data":
                        #         {
                        #             "src": "9.9.9.9",
                        #         },
                        #         "rest_data":[]
                        # }
                    }, 



               # "send_data":
               #      {
               #          #"iface": "eth1",
               #          "sleep": 1,
               #          "verbose":0,
               #      }
        },
            {
                "direction": "outbound",
                "id":1,
                "pcap_data":
                    { 
                        "NTPPrivate":
                        {
                            "update_data":
                                {
                                    "version": 4,
                                }
                        },
                    }, 
        }        
    ]
    for i in a:
        obj = generate_data(i)
        data = obj.make_data()
        pprint(data)
        obj = handle_pcap(sys.argv[1])
        obj.relay_private_pcap_by_scapy([data])
