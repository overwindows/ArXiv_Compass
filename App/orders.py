# coding:utf-8

import os
import web
import model
import time
import datetime
import json
import sign
import urllib
import logging
from env import *

# 订单页
class orders:
    def GET(self):
        user_info = web.ctx.session.userinfo
        if user_info.has_key("ID"):
            uid = user_info["ID"]
            orders_0 = model.get_orders(int(uid), 0)
            orders_1 = model.get_orders(int(uid), 1)
            orders_2 = model.get_orders(int(uid), 2)
            return render.orders(orders_0, orders_1, orders_2)
        else:
            web.ctx.session.redirecturl = "/orders"
            web.seeother('/login')
	'''
        islogin = False
        try:
            if web.ctx.session.userid:
                islogin = True
            else:
                islogin = False
        except AttributeError:
            islogin = False
        if islogin:
            msgs = []
            userid = web.ctx.session.userid
            orders_0 = model.get_orders(int(userid), 0)
            orders = list(orders_0)
            logging.debug('userid:' + userid)
            msgs_it = model.ongoing_orders_cnt(userid)
            msgs = list(msgs_it)
            deadline_ts = {}
            for o in orders:
                deadline_ts[o.id] = int(time.mktime(time.strptime(str(o.orderdate) + " 10:30:00", "%Y-%m-%d %H:%M:%S")))
            cur_timestamp = int(time.time())
            return render.order_index(userid, orders, cur_timestamp, deadline_ts, web.ctx.session.headimgurl,
                                      web.ctx.session.nickname, msgs)
        else:
            msg = None
            web.setcookie('url', '/order_index', 3600)
            return render.login_index(msg)
    '''
