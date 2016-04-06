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
from pay import *

class prepay:
    def GET(self):
        #i = web.input()
        #pay_id = i.payid
        #web.ctx.session.payid = pay_id 
        #print pay_id       
        redir_url='http%3a%2f%2fm.zhunshikaifan.com%2fwebchatpay'
        js_api = JsApi_pub()
        prepay_url = js_api.createOauthUrlForCode(redir_url)
        return web.seeother(prepay_url)
