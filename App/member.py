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
class member:
    def GET(self):
        user_info = web.ctx.session.userinfo
        nick_name = web.ctx.session.nickname
        headimg_url = web.ctx.session.headimgurl

        if user_info.has_key("ID"):
            return render.member(user_info, nick_name, headimg_url)
        else:
            return web.seeother('/anonymous')
	'''	
    def POST(self):
        msg = None
        i = web.input()
        uid = i.get('userid')
        pwd = i.get('password')
        user_iter=model.get_user(uid,pwd)
        user = list(user_iter)        
        if user:
            web.setcookie('username', user[0].username, 3600)
            web.setcookie('userid',uid, 3600)
            web.setcookie('contactname', user[0].contactname, 3600)
            web.setcookie('unitaddress', user[0].unitaddress, 3600)
            web.ctx.session.username = user[0].username
            web.ctx.session.userid = uid
            next_page = web.cookies().get('url')
            #print next_page
            web.ctx.session.logged_in = True
            web.setcookie('backstep',-2,3600)                
            
            return web.seeother(next_page)
        else:
            msg="用户名或密码不正确"
            web.setcookie('login_id',uid,3600)
            return render.login_index(msg)
	'''