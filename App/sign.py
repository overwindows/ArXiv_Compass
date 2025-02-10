import time
import random
import string
import hashlib
import urllib2
import json

class Sign:
    def __init__(self, jsapi_ticket, url):
        self.ret = {
            'nonceStr': self.__create_nonce_str(),
            'jsapi_ticket': jsapi_ticket,
            'timestamp': self.__create_timestamp(),
            'url': url
        }

    def __create_nonce_str(self):
        return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(15))

    def __create_timestamp(self):
        return int(time.time())

    def sign(self):
        string = '&'.join(['%s=%s' % (key.lower(), self.ret[key]) for key in sorted(self.ret)])
        print string
        self.ret['signature'] = hashlib.sha1(string).hexdigest()
        return self.ret

def get_token():
    url="https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=wx9e8d00301079061b&secret=6021e0985185092b430c4182db3b3f62"
    data = urllib2.urlopen(url).read()
    #print url
    return json.loads(data)['access_token']

def get_ticket(access_token):
    url='https://api.weixin.qq.com/cgi-bin/ticket/getticket?access_token='+access_token+'&type=jsapi'
    data = urllib2.urlopen(url).read()
    #print url
    return json.loads(data)['ticket']
