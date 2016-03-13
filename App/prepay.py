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
        i = web.input()
        oid = i.orderid
        logging.debug("[orderid:%s]", str(oid))
        web.ctx.session.pay_oid = oid        
        redir_url='http%3a%2f%2fm.zhunshikaifan.com%2fpayment'
        js_api = JsApi_pub()
        prepay_url = js_api.createOauthUrlForCode(redir_url)
        #print prepay_url
        return web.seeother(prepay_url)
