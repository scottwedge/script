import os,time
second = 3
user_add = 1
idle_add= 6
num=0;num1=0
os.system(r"sed -i 's/echo [0-9].*/echo 0/g' /root/TFTP/snmp-cpu-temp_idle")
while True:
    num = 0 if num > 1000 else num + user_add 
    num1 = 0 if num1 > 1000 else num1 + idle_add 
    cmd1 = r"sed -i 's/echo [0-9].*/echo %s/g' /root/TFTP/snmp-cpu-temp" %(num)
    cmd2 = r"sed -i 's/echo [0-9].*/echo %s/g' /root/TFTP/snmp-cpu-temp_idle" %(num1)
    cmd =  cmd1+';'+cmd2  
    print cmd   
    os.system(cmd)   