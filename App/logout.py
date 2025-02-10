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

#退出当前账户
class logout:
    def GET(self):
        #print web.ctx.session.openid
        #print web.ctx.session.nickname
        #print web.ctx.session.headimgurl
        param = urllib.urlencode({'openid':web.ctx.session.openid,'nickname':web.ctx.session.nickname.encode("utf8"),'headimgurl':web.ctx.session.headimgurl})
        web.setcookie('username', '', expires=-1)
        web.setcookie('userid', '', expires=-1)
        try:
            #web.setcookie('weixin_nickname',session.nickname, 3600)
            #web.setcookie('weixin_headimgurl',session.headimgurl, 3600)
            web.ctx.session.kill()
            web.ctx.session.session.logged_in = False
        except AttributeError:
            pass

        return web.seeother("http://x.zhunshikaifan.com/?"+param)
