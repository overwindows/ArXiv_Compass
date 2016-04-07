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

class webchatpay:
    def GET(self):
        global access_token
        global jsapi_ticket
        global token_timestamp

        js_api = JsApi_pub()
        openid = "oTb7Zs6117TYsKwBccbut4UaFAhs"
        #print openid
        if (not access_token.strip()) or (int(time.time())-token_timestamp > 7200):
            access_token = sign.get_token()
            jsapi_ticket = sign.get_ticket(access_token)
            token_timestamp = int(time.time())

        #oid = session.pay_oid
        #print oid
        #order_it = model.get_order(oid)
        #order = list(order_it)

        js_sign = Sign(jsapi_ticket, web.ctx.home+web.ctx.fullpath)
        sign_data = js_sign.sign()
        nonceStr = sign_data['nonceStr']
        signature = sign_data['signature']
        timestamp = sign_data['timestamp']
        url = sign_data['url']
        #print url
        #total_fee = web.cookies().get('total_price')
        #total_fee = str(int(order[0].Price)*100)  #TODO:dup orderid
        unify_pay = UnifiedOrder_pub()
        #print oid
        #print total_fee
        #print openid
        unify_pay.setParameter('out_trade_no','137742589700')
        unify_pay.setParameter('body','准时开饭 套餐')
        unify_pay.setParameter('total_fee','1')
        unify_pay.setParameter('notify_url','http://m.zhunshikaifan.com/carte_succeed')
        unify_pay.setParameter('trade_type','JSAPI')
        unify_pay.setParameter('openid',openid)
        prepay_id = unify_pay.getPrepayId()
        #print prepay_id

        js_api.setPrepayId(prepay_id)
        pay_data = js_api.getParameters()

        return render.webchatpay(signature,nonceStr,timestamp,json.loads(pay_data))
