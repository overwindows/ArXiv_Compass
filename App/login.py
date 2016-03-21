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

#Login Page
class login:
    def GET(self):
        msg = None
        web.ctx.session.logged_in = True
        return render.login()
    def POST(self):
        msg = None
        i = web.input()
        uid = i.get('userid')
        pwd = i.get('password')
        
        user_iter=model.get_user(uid,pwd)
        user = list(user_iter)
        user_info = web.ctx.session.userinfo
        if user:
            user_info['Name'] = user[0].username
            user_info['ID'] = uid
            user_info['Contact'] = user[0].contactname
            user_info['UnitAddr'] = user[0].unitaddress
            user_info['Tel'] = user[0].tel

            redirect_url = web.ctx.session.redirecturl
            #print next_page
            web.ctx.session.logged_in = True
            web.setcookie('backstep',-2,3600)
            
            return web.seeother(redirect_url)
        else:
            msg="用户名或密码不正确"
            web.setcookie('login_id',uid,3600)
            return render.login()
