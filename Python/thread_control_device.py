import os
import threading 
import time
def fun(ip):
    while True:
        print '%s start'%ip
        check = os.popen(r"ssh root@%s sipp -v"%ip)
        if 'v3.3'  in check.read():
            print '%s pass'%ip
            os.system(r"ssh root@%s sed -i \'s/^^#nameserver 180.76.76.76/#nameserver 180.76.76.76/\' /etc/resolv.conf"%ip)
            break
        else:
            os.system("ssh root@%s killall -9 yum"%ip)
            os.system(r"ssh root@%s sed -i \'s/#nameserver 180.76.76.76/nameserver 180.76.76.76/\' /etc/resolv.conf"%ip)
            cmd = r"ssh root@%s yum install sipp -y >> /dev/null"%ip 
            os.system(cmd)
        time.sleep(5)

         
l = [1,2,3,8,9,10]
k = 0
for i in range(11):
    for j in l :
        ip = '10.0.200.'+str(j+k)
        t = threading.Thread(target=fun,args=(ip,))
        t.start()
    k += 20   
