#coding:utf-8

import os
import web
import model
import time
import datetime
import json
import sign
import urllib

from env import *

#Register Page & Forget Pass
class register:
    def GET(self):
	    return render.register()
    '''
    def GET(self):        
        i = web.input()
        uid = i.get('id')
        flag = i.get('flag')
        web.ctx.session.reg_flag = flag                
        #print uid
        web.ctx.session.valid_sms=37194
        return render.register_index(uid,flag,0)
    def POST(self):
        i = web.input()
		#新用户注册 or 密码重置
        action = i.get('type')
        print action        
        password = i.get('password')
        phone = i.get('telephone')
        sms = i.get('valid_sms')
        #print sms       
        #check if the phone num is exist.        
        dup_usr = list(model.reg_dup_check(phone))
        
        username = web.ctx.session.nickname
        if action=="reg":
            if dup_usr:
                return render.register_index(0,0,1)
            valid_sms=web.ctx.session.valid_sms
            print valid_sms
            try:
                if int(valid_sms)==int(sms):
                    model.new_user(phone,username,password,web.ctx.session.openid,time.strftime('%Y-%m-%d %X', time.localtime()))
                else:
                    return render.register_index(0,0,2)
            except ValueError:
                return render.register_index(0,0,2)
        elif action=="reset":
            #print phone
            if not dup_usr:
                print "user not exist!!"
                return render.register_index(0,1,3)
            valid_sms=web.ctx.session.valid_sms
            try:
                if int(valid_sms)==int(sms):
                    model.new_pass(phone,password)
                else:
                    return render.register_index(0,0,2)
            except ValueError:
                return render.register_index(0,1,2)
            
        web.setcookie('username', username, 3600)
        web.setcookie('userid', phone, 3600)
        web.ctx.session.username = username
        web.ctx.session.userid = phone
        web.setcookie('login_id','',expires=-1)
        previous = web.cookies().get('url')
        #print ":"+str(previous)
        if action=="reg":
            return web.seeother(previous)
        elif action=="reset":
            print "reset pass success!"
            #return web.seeother("/index?code=Fake")
            return web.seeother("/wechat")
	'''