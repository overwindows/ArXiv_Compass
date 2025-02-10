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

# Order Detail
class orderinfo:
    def GET(self):
        info = {}
        i = web.input()
        oid = i.get('oid')
        o_details = list(model.get_detail(oid))
        o_info = list(model.get_order(oid))
        info["i"] = o_info[0]
        info["d"] = o_details
        '''
        opt = i.get('opt')

        ot_ts = int(time.mktime(time.strptime(str(ord_info[0].OrderDate)+" 10:30:00", "%Y-%m-%d %H:%M:%S")))
        cur_ts = int(time.time())
        if cur_ts > ot_ts:
            OT=True
        else:
            OT=False
        '''
        return render.orderinfo(info)
