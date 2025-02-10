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

#Order Rollback 
class cancelorder:
    def GET(self):
        i = web.input()
        oid = i.get('oid')
        order = model.get_order(oid)
        orderdate = list(order)[0].OrderDate
        details = model.get_details(oid)
        for detail in details:
            model.upd_meal_sold(detail.lunchid,orderdate,-detail.num)
            
        model.update_order(oid, 2, time.strftime('%Y-%m-%d %X', time.localtime()))                
        #print oid
        #refund = Refund_pub()
        #refund.setParameter('transaction_id')
        #refund.setParameter('out_trade_no',str(session.out_trade_no))
        #refund.setParameter('out_trade_no','1234567890')
        #refund.setParameter('total_fee','1')
        #refund.setParameter('refund_fee','1')
        #refund.setParameter('out_refund_no','1234567890')
        #refund.setParameter('op_user_id','1240046802')

        #res = refund.getResult()
        #print res["return_code"]
        #print res["return_msg"]
        return web.seeother('/orders')