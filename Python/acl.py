#!/home/zcyang/git/script/Python/venv/bin/python

from ddos import Control_ddos
import sys
aclname = "acl1"
if __name__ == "__main__":
    ar = sys.argv
    ob = Control_ddos("10.0.100.114")
    if ar[1] == "s1":
        print(ob.send_command("show ddos global acl-ipv4"))

    if ar[1] == "s2":
        print(ob.send_command("show ddos global address4"))

    if ar[1] == "s3":
        print(ob.send_command("show ddos global addressgrp"))

    if ar[1] == "s4":
        print(ob.send_command("show ddos global service"))

    if ar[1] == "d1":
        args = {"variable_dict": {"aname": ar[2]}, "template": "del_acl.txt"}
        print(ob.control_config(**args))

    if ar[1] == "d2":
        args = {"variable_dict": {"aname": ar[2]}, "template": "del_address.txt"}
        print(ob.control_config(**args))

    if ar[1] == "d3":
        args = {"variable_dict": {"gname": ar[2]}, "template": "del_group.txt"}
        print(ob.control_config(**args))

    if ar[1] == "d4":
        args = {"variable_dict": {"sname": ar[2]}, "template": "del_service.txt"}
        print(ob.control_config(**args))

    if ar[1] == "a11":
        args = {"variable_dict": {"aname": aclname, "sname": ar[2]}, "template": "add_acl_sourcea.txt"}
        print(ob.control_config(**args))

    if ar[1] == "a12":
        args = {"variable_dict": {"aname": aclname, "gname": ar[2]}, "template": "add_acl_sourceg.txt"}
        print(ob.control_config(**args))

    if ar[1] == "a13":
        args = {"variable_dict": {"aname": aclname, "sname": ar[2]}, "template": "add_acl_dsta.txt"}
        print(ob.control_config(**args))

    if ar[1] == "a14":
        args = {"variable_dict": {"aname": aclname, "gname": ar[2]}, "template": "add_acl_dstg.txt"}
        print(ob.control_config(**args))

    if ar[1] == "a15":
        args = {"variable_dict": {"aname": aclname, "sname": ar[2]}, "template": "add_acl_service.txt"}
        print(ob.control_config(**args))

    if ar[1] == "a16":
        args = {"variable_dict": {"aname": aclname, "gname": ar[2]}, "template": "add_acl_serviceg.txt"}
        print(ob.control_config(**args))

    if ar[1] == "a2":
        args = {"variable_dict": {"aname": ar[2], "ip": ar[3]}, "template": "add_address_mask.txt"}
        print(ob.control_config(**args))

    if ar[1] == "a21":
        args = {"variable_dict": {"aname": ar[2], "sip": ar[3], "bip": ar[4]}, "template": "add_address_range.txt"}
        print(ob.control_config(**args))

    if ar[1] == "a3":
        args = {"variable_dict": {"gname": ar[2], "sname": ar[3]}, "template": "add_group.txt"}
        print(ob.control_config(**args))

    if ar[1] == "a41":
        args = {"variable_dict": {"sname": ar[2], "sport": ar[3], "bport": ar[4]}, "template": "add_service_dport.txt"}
        print(ob.control_config(**args))

    if ar[1] == "a42":
        args = {"variable_dict": {"sname": ar[2], "sport": ar[3], "bport": ar[4]}, "template": "add_service_sport.txt"}
        print(ob.control_config(**args))

    if ar[1] == "a43":
        args = {"variable_dict": {"sname": ar[2], "type": ar[3]}, "template": "add_service_type.txt"}
        print(ob.control_config(**args))
