#!/usr/bin/python3

from scapy.all import *
import argparse
import sys
from pprint import pprint
import traceback
import time
import yaml 
from jinja2 import Template


global TRACEINFO 
TRACEINFO = '#####\n'

DEFAULT_FUN_DICT = {"RANDIP": RandIP().ip.choice(),
                    "RANDPORT": int(RandNum(1024, 65536)),
                   }

def my_constructor(loader, node):
    value = loader.construct_scalar(node)
    return eval(value)

yaml.add_constructor(u'!EVAL', my_constructor)

 

class StoreDictKeyPair(argparse.Action):
     def __call__(self, parser, namespace, values, option_string=None):
         my_dict = {}
         for kv in values.split(","):
             k,v = kv.split("=")
             my_dict[k] = v
         setattr(namespace, self.dest, my_dict)




class tool(object):
    def get_ip_mac(port):
        ip = get_if_addr(port)
        mac = get_if_hwaddr(port)
        return (mac, ip)
        
class template_parse(object):
    def __init__(self, template):
        self.template = template


    def parse_yaml(self, variable_dict = {}):
        try:
            fp = open(self.template, 'r')
            data = fp.read()
            fp.close()
            template = Template(data)
            variable_dict.update(DEFAULT_FUN_DICT)
            data_handle = template.render(**variable_dict)
            result = yaml.load(data_handle, Loader = yaml.FullLoader)
        except Exception as e:
            print("parse yaml error %s"%(str(e)))
            raise
            sys.exit(0)
            #raceback.print_exc()            
        return result 


class generate_pkt(object):
    def __init__(self):
        self.topo_info = self.get_topo_info()

    def get_topo_info(self):
        topo_info = {
            "client":
                 {"iface": "eth1",
                  "addr": tool.get_ip_mac("eth1")
                 },
            "server":
                 {"iface": "eth2",
                  "addr": tool.get_ip_mac("eth2")
                 }
            }
        return topo_info

    def generate(self, data):
        option = data.get("option")
        pcap_info = data.get("pcap_info")
        send_info = data.get("send_info")
        if(option.get("direction", "inbound") == "outbound"):
            riface, siface = self.topo_info["client"]["iface"], self.topo_info["server"]["iface"]
            daddr, saddr = self.topo_info["client"]["addr"], self.topo_info["server"]["addr"]
        else:
            siface, riface = self.topo_info["client"]["iface"], self.topo_info["server"]["iface"]
            saddr, daddr = self.topo_info["client"]["addr"], self.topo_info["server"]["addr"]
        send_info.setdefault("riface", riface)
        send_info.setdefault("siface", siface)

        pkt = Ether(src = saddr[0], dst = daddr[0])/IP(src = saddr[1], dst = daddr[1])
        for info in pcap_info:
            for layer, layerinfo in info.items():
                layer_obj = pkt.getlayer(eval(layer))
                if not layer_obj:
                    pkt.add_payload(eval(layer)())
                    layer_obj = pkt.getlayer(eval(layer))
                if layerinfo is None:
                    continue
                for key, value in layerinfo.items():
                    layer_obj.setfieldval(key, value)
        return pkt


class send_pcap(object):
    def __init__(self):
        pass
    def send(self, pkt, send_info):
        t = AsyncSniffer(iface = send_info["riface"])
        t.start()
        time.sleep(0.2)    
        sendp(pkt, iface = send_info["siface"])
        #os.system("date")
        res = t.stop()

        verbose = send_info.get("verbose", None)
        print("recv %d packets"%len(res));
        global TRACEINFO
        cache =  os.popen('python3 /home/script/tmp.py s2').read()
        cache = cache.replace("\n\n",'\n').replace(" \n/#", "\n")
        print("cache info\n", cache)
        TRACEINFO = TRACEINFO + cache

        """
        slen = len(pkt)
        rlen = len(res)
        if(slen != rlen):
            print("!!!!!! send %d packets recieve %d packets loss %d packets "%(slen, rlen, slen - rlen))
        else:
            print("###### send %d packets recieve %d packets loss %d packets "%(slen, rlen, slen - rlen))
        """
        if verbose:
            for pkt in res:
                layer = pkt.getlayer(eval(verbose))
                result = layer.show2(dump = True)
                print(result)

        else:
            res.nsummary()
            
        sleep_time = send_info.get("sleep", 0)
        if sleep_time:
            time.sleep(sleep_time)

class handle_result(object):
    pass


class handle_process(object):
    def __init__(self, data):
        self.data = data
        self.pkt_list = []
            

    def generate_pkts(self):
        gen_obj = generate_pkt()
        for i in self.data:
            i["option"] = i.get("option") or {}
            i["send_info"] = i.get("send_info") or {}
            pkt = gen_obj.generate(i)
            self.pkt_list.append(pkt)

    def send_pcaps(self):
        for pkt, data_info in zip(self.pkt_list, self.data):
            send_info = data_info.get("send_info", {})
            send_pcap().send(pkt, send_info)

    def handle_one_yaml(self):
        #([spkts, rpesponse_pkts], recieve_pkts)send_pcaps(data)
        self.send_pcaps()

    def run(self):
    	self.generate_pkts()		
    	result = self.handle_one_yaml()
                #handle_result(result)
    	#return result

def main(args):
    """
    template = args.yaml
    variable_dict = args.var or {}
    template_data = template_parse(template).parse_yaml(variable_dict)
    handle_process().run(template_data)
    """
    template = args.yaml
    variable_dict = args.var or {}
    template_data = template_parse(template).parse_yaml(variable_dict)
    handle_process(template_data).run()
	

def usage():
    parser = argparse.ArgumentParser(description='replay pcap')
    parser.add_argument('yaml', help ="yaml file")
    parser.add_argument('-test', type=int, help ="test option")
    parser.add_argument("--var", dest="var", action=StoreDictKeyPair, metavar="KEY1=VAL1,KEY2=VAL2...")
    args = parser.parse_args()
    return args

def test(args):
    if args.test == 1:
        template = args.yaml
        variable_dict = args.var or {}
        template_data = template_parse(template).parse_yaml(variable_dict)
        print(template_data)

    if args.test == 2:
        template = args.yaml
        variable_dict = args.var or {}
        template_data = template_parse(template).parse_yaml(variable_dict)
        handle_process(template_data).generate_pkts()

    if args.test == 3:
        template = args.yaml
        variable_dict = args.var or {}
        template_data = template_parse(template).parse_yaml(variable_dict)
        handle_process(template_data).run()
    #if args.test == 4:
    template = args.yaml
    variable_dict = args.var or {}
    template_data = template_parse(template).parse_yaml(variable_dict)
    handle_process(template_data).run()  
    global TRACEINFO
    print(TRACEINFO)
    

if __name__ == "__main__":
    args = usage()
    test(args)

