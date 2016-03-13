#coding:utf-8

import os
import web
import model
import time
import datetime
import json
import sign
import urllib
import random
import urllib2

from env import *

class sms_valid:
    def GET(self):
        i = web.input()
        mobile=i.get("mobile")
        #判断是新注册还是密码重置
        flag = web.ctx.session.reg_flag
        dup_usr = list(model.reg_dup_check(mobile))
        #print '[DEBUG]<sms_valid> flag='+flag
        print mobile        
        if flag is None:  
            if dup_usr:
                return "该号码已注册"
        elif int(flag)==1:
            if not dup_usr:
                return "该号码未注册"
        #print '你好2008'.decode("UTF-8").encode("GBK").encode("hex")
        valid_msg=random.randint(10000, 100000)
        short_msg='您的验证码:'.decode("UTF-8").encode("GBK")+str(valid_msg)
        #short_msg=('您的验证码:'+str(valid_msg)).decode("UTF-8").encode("GBK")
        #short_msg='您的验证码:37194'.decode("UTF-8").encode("GBK")
        #http://esms.etonenet.com/sms/mt?command=MT_REQUEST&spid=3029&sppassword=amxx3029&da=8613501927419&dc=15&sm=c4e3bac332303038
        url = 'http://esms.etonenet.com/sms/mt' 
        payload='command=MT_REQUEST&spid=7700&sppassword=amxx7700&da=86'+str(mobile)+'&dc=15&sm='+short_msg.encode("hex")
        print payload
        web.ctx.session.valid_sms=valid_msg
        print urllib2.urlopen(url, payload).read()
        return "success"