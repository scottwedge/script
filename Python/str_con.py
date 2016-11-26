import random
import os
import sys
import time
num = 20 
second = 0.01
name_interupt = 'interupt'
name = 'user'
while True:
    try:
        num_new = random.randint(1,20)
        cmd = r"sed -i 's/echo %s/echo %s/g' /root/TFTP/snmp-cpu_%s-temp" %(num,num_new,name)
        os.system(cmd)
        print cmd        
        num = num_new
        time.sleep(second)
    except KeyboardInterrupt:
        cmd = r"sed -i 's/echo [0-9].*/echo 20/g' /root/TFTP/snmp-cpu_%s-temp" %(name,)
        print 'aaa' 
        os.system(cmd)
        sys.exit()