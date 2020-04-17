#/bin/python

from ddos import Control_ddos
import sys
aclname = "sppip"
if __name__ == "__main__":
    ar = sys.argv
    ob = Control_ddos("10.0.100.114")
    if len(ar) == 1 or ar[1] in ["-h", "-help"]:
        print("""
            s1      show ddos spp ip profile
            a1      modify anomaly status      para:pname status
            """)
        sys.exit(0)
    if ar[1] == "s1":
        print(ob.send_command("show full ddos spp ip profile"))

    if ar[1] == "a1":
        t_name = aclname + "/ip_anomaly.txt"
        args = {"variable_dict": {"pname": ar[2], "status": ar[3]}, "template": t_name}
        print(ob.control_config(**args))

