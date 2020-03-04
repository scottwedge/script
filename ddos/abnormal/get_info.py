#!/bin/python
import os
import re

def get_mac_and_ip(port):
    fb = os.popen("ip addr show %s" %port)
    data = fb.read()
    pattern = re.compile(r'ether ((?:(?:[0-9a-f]{2}[:]){5})[0-9a-f]{2}).*inet ((?:(?:[0-9]{1,3}\.){3}[0-9]{1,3}))/', re.IGNORECASE|re.S)
    infos = pattern.search(data).groups()
    if len(infos) == 2:
        mac, ip = infos
    return mac, ip 

