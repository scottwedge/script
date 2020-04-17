#!/home/zcyang/git/script/Python/venv/bin/python
from robot.libraries.Telnet import Telnet
from get_template import get_settings
import sys
import time

class Control_ddos():
    def __init__(self, ip, username='admin', pwd='fortinet', port=23):
        self.ip = ip
        self.username = username
        self.pwd = pwd
        self.port = 23
        self.telnet_instance = Telnet(timeout=8, default_log_level='TRACE')
        option = {}
        option["host"] = self.ip
        option["port"] = self.port
        option["default_log_level"] = "trace"
        option["alias"] = "ddos1"
        option["prompt"] = r"(\r\n)?(/|FortiDDoS|FI-FDD).*#|.*y\/n\)"
        option["prompt_is_regexp"] = True
        self.telnet_instance.open_connection(**option)
        self.telnet_instance.login(self.username, self.pwd)


    def control_config(self, **args):
        config_settings = get_settings(**args)
        output = ''
        print("command is %s\n" %config_settings)
        n = len(config_settings)
        output = ''
        for i in range(n):
            print("command   $%s$"%config_settings[i])
            self.telnet_instance.write(config_settings[i])
            # output = self.telnet_instance.read_until_prompt()
            # print("output  $%s$"%repr(output))
            if i == n - 1:
                output = self.telnet_instance.read_until_prompt()
        return output

    def send_command(self, command, shell = False):
        if shell:
            self.telnet_instance.write("fn sh")
            output = self.telnet_instance.read_until_prompt()            
        self.telnet_instance.write(command)
        output = self.telnet_instance.read_until_prompt()
        return output

if __name__ == "__main__":
    ar = sys.argv
    args = {"variable_dict":{"aname":ar[2], "ip":ar[3]}, "template":ar[1]}
    ob = Control_ddos("10.0.100.114")
    print(ob.control_config(**args))
    print("delete file \n")
    args = {"variable_dict":{"aname":ar[2]},  "template": "del_address.txt"}
    print(ob.control_config(**args))



