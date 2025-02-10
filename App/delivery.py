#coding:utf-8

import os
import web
import model
import time
import datetime
import json
import sign
import urllib
import uuid

from env import *

class delivery:
    def GET(self):
        user_info = web.ctx.session.userinfo
        return render.delivery(user_info)
    def POST(self):
        user_info = web.ctx.session.userinfo
        i = web.input()
        tel = i.get('telephone')
        contact = i.get('contact')
        unitaddress = i.get('unitaddress')
        invoice = i.get('invoice')
        if user_info.has_key("ID"):
            model.update_username(user_info["ID"], contact, web.ctx.session.officeid, unitaddress, tel)
        else:
            dup_usr = list(model.reg_dup_check(tel))
            if dup_usr:
                model.new_user(uuid.uuid1(),web.ctx.session.nickname,web.ctx.session.openid,contact,web.ctx.session.officeid, unitaddress,time.strftime('%Y-%m-%d %X', time.localtime()))
            else:
                model.new_user(tel,web.ctx.session.nickname,web.ctx.session.openid,contact,web.ctx.session.officeid, unitaddress,time.strftime('%Y-%m-%d %X', time.localtime()))
        user_info["Contact"] = contact
        user_info["Tel"] = tel
        user_info["Invoice"] = invoice
        user_info["UnitAddr"] = unitaddress
        user_info["ID"] = tel
        web.ctx.session.userinfo = user_info

        return web.seeother('/bill')

