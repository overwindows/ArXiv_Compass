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
        unit_address = i.get('unit_address')

        model.update_username(user_info["ID"], contact, web.ctx.session.officeid, unit_address)
        user_info["Contact"] = contact
        user_info["Tel"] = tel
        web.ctx.session.userinfo = user_info

        return web.seeother('/bill')