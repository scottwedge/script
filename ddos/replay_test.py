from replay_pcap import *

def usage_test():
    parser = argparse.ArgumentParser(description='replay pcap')
    parser.add_argument('--yaml', default="template.yml",help ="yaml file")
    parser.add_argument('--pcap', default="/home/pcap/ntp/ntp_private.pcap", help ="replay pcap")
    parser.add_argument("--var", dest="var", action=StoreDictKeyPair, metavar="KEY1=VAL1,KEY2=VAL2...")
    args = parser.parse_args()
    return args

if __name__ == "__main__":

    args = usage_test()

    pcap_name = args.pcap
    yaml_name = args.yaml
    variable_dict = args.var or {}
    print(pcap_name, yaml_name, variable_dict)

    yaml_data = tool.parse_yaml(yaml_name, variable_dict)
    for i in yaml_data:
        obj = generate_data(i)
        data = obj.make_data()
        pprint(data)
        obj = handle_pcap(pcap_name)
        obj.relay_private_pcap_by_scapy([data])
