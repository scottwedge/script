import os

def fun():
    l = [1,2,3,8,9,10]
    k = 0
    for i in range(11):
        for j in l :
            ip = '10.0.200.'+str(j+k)
            os.system(r'sshpass -p fortinet ssh-copy-id -i ~/.ssh/id_rsa.pub root@%s -o "StrictHostKeyChecking no"'%ip)
        k += 20
def fun1():
    l = [1,2,3,8,9,10]
    k = 0
    for i in range(11):
        for j in l :
            ip = '10.0.200.'+str(j+k)
            print ip 
            check = os.popen(r"ssh root@%s sipp -v"%ip)
            if 'v3.3'  in check.read():
                print 'pass'
            else:
                os.system("ssh root@%s killall -9 yum"%ip)
                os.system(r"ssh root@%s sed -i \'s/#nameserver 180.76.76.76/nameserver 180.76.76.76/\' /etc/resolv.conf"%ip)
                cmd = r"ssh root@%s yum install sipp -y"%ip
                os.system(cmd)
        k += 20    
while True:
    fun1()
