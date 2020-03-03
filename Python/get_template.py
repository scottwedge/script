import os
import sys
from jinja2 import Template

basename = "/home/zcyang/fortinet/ddos/autotest/config"
dirname = "acl"

def get_settings(**args):
    template_file = args.get('template')
    variable_dict = args.get('variable_dict', {})
    fname = os.path.join(basename, dirname, template_file)
    print(fname)
    fp = open(fname, 'r')
    data = fp.read()
    fp.close()
    template = Template(data)
    data_handle = template.render(**variable_dict)
    current_setting = data_handle.split("\n")
    current_setting = [commnad.strip() for commnad in current_setting]
    current_setting.append(current_setting[0].replace('config','show'))
    return current_setting

if __name__ == "__main__":
    ar = sys.argv
    args = {"variable_dict":{"aname":ar[1], "ip":ar[3]}, "template":ar[1]}
    get_settings(**args)
