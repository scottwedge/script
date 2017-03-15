s = {u'--suite': u'aaaaaaaaaa', u'-v': u'lab:DevLab2', u'--test': u'cccccccccccc', u'--log': u'bbbbbbbbbb'}


l1 =  map(lambda x:x[0] +x[1],s.items())
l2 = ['robot','a','b']


l1 = []



print list(reduce(lambda x,y:x+y,s.items()))








for k,v in s.items():
    l1 = l1 + [k,v]
print l1    

