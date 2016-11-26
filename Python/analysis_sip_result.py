import os
import re
dir = '/root/TFTP/'
file = os.path.join(dir,'sipp.log')

l=[]
pattern = re.compile(r'SIP/2.0 200 OK\r\n.*?\r\n\r\n', re.S)
with open(file) as f:
    data = f.read()
m = re.findall(pattern,data)
for i in m:
    m = i.split('\r\n')
    print m

