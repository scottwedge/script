import requests
import json
auth = ('zcyang@fortinet.com','neteye')
auth_adc = ('admin','')
url_adc = 'http://10.0.100.134'

def get():
    r = requests.get(url_adc+'/api/system_global',auth=auth_adc)
    print r.status_code
    value =  r.json()
    
def post():
    payload = {'body':'hhal'}
    r = requests.post(url_adc+'/api/v1.0/posts/',json=payload,auth=auth)
    print r.status_code
    value =  r.json()
    print value
    
    
def put(id):
    payload = {'body':'hhal1111aaaaaaaaa'}
    r = requests.put(url_adc+'/api/v1.0/posts/%s'%str(id),json=payload,auth=auth)
    print r.status_code
    value =  r.json()
    print value    
#post()
#get()
get()