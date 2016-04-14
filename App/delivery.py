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

        model.update_username(user_info["ID"], contact, web.ctx.session.officeid, unitaddress, tel)
        user_info["Contact"] = contact
        user_info["Tel"] = tel
        user_info["Invoice"] = invoice
        user_info["UnitAddr"] = unitaddress
        web.ctx.session.userinfo = user_info

        return web.seeother('/bill')
