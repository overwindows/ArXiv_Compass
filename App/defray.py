#coding:utf-8

import os
import web
import model
import time
import datetime
import json
import sign
import urllib
import random

from env import *

#Pay Launch
class defray:
    def GET(self):
        shopping_basket = web.ctx.session.shoppingbasket
        shopping_list = web.ctx.session.shoppinglist
        user_info = web.ctx.session.userinfo
        shopping_cost = web.ctx.session.shoppingcost
        seed_no = int(time.time())
        invoice = user_info["Invoice"]

        i = web.input()
        param = i.get("param")
        print param
        order_info = {}
        order_list = param.split("|")
        for order in order_list:
            if order:
                id,tm = order.split("_")
                order_info[str(id)] = tm
        #print order_info.keys()

        id = 0
        for _date in shopping_basket:
            id = id + 1
            _id = str(id) 
            if order_info.has_key(_id):
                rand_suffix = random.randint(1000,10000)
                orderid = seed_no * 1000 + rand_suffix
                shopping_list.append(str(orderid))
                allcnt = 0
                for item in shopping_basket[_date]:
                    allcnt += int(shopping_basket[_date][item]["Count"])
                #if failed in next steps, the order should be deleted!!!
                model.new_order(orderid,user_info["Tel"], user_info["Contact"], user_info["OfficeId"], _date, \
                            float(shopping_cost[_date]["price"]), float(shopping_cost[_date]["price0"]),float(shopping_cost[_date]["price1"]),\
                            float(shopping_cost[_date]["price2"]), allcnt , time.strftime('%Y-%m-%d %X', time.localtime()),\
                            time.strftime('%Y-%m-%d %X', time.localtime()),user_info["ID"],\
                            invoice, user_info["UnitAddr"], order_info[_id])
                lidict = {}
                for _lunchid in shopping_basket[_date]:
                    cnt = shopping_basket[_date][_lunchid]["Count"]
                    meal_it = model.get_meal_detail(_lunchid, _date)
                    meal_dtl = list(meal_it)

                    if int(meal_dtl[0].stock) >= int(cnt):
                            #新增订单详情
                        model.new_detail(orderid, _lunchid, cnt)
                            #库存修改
                        ret = model.upd_meal_sold(_lunchid,_date,cnt)
                            #print 'upd_meal_sold return:'+str(ret)
                        if ret == -1:
                            web.ctx.session.failreason = "stock"
                            model.del_order(orderid)
                            model.del_detail(orderid)
                            for (k,v) in lidict.items():
                                model.upd_meal_sold(k,_date,-int(v))
                            return web.seeother('/orderfail')
                        elif ret == 0:
                                #暂存已更新的库存信息
                            lidict[_lunchid] = cnt
                    else:
                        web.ctx.session.failreason="stock"
                        model.del_order(orderid)
                        model.del_detail(orderid)
                        for (k,v) in lidict.items():
                            model.upd_meal_sold(k,_date,-int(v))
                        return web.seeother('/orderfail')
        #print shopping_list
        oids = "_".join(shopping_list)

        # clear shopping_basket and shopping cost
        if web.ctx.session.shoppingbasket:
            web.ctx.session.shoppingbasket.clear()
        if web.ctx.session.shoppingcost:
            web.ctx.session.shoppingcost.clear()

        return web.seeother('/webchatpay?oids=' + oids)
'''
        # 超时无法下单（判断当日套餐的支付时间是否超过10:32）Start
        ot_ts  = int(time.mktime(time.strptime(str(web.ctx.session.menu_date)+" 10:32:00", "%Y-%m-%d %H:%M:%S")))
        cur_ts = int(time.time())
        if cur_ts > ot_ts:
            web.ctx.session.failreason="expired"
            return web.seeother('/carte_failed')
        # End

        #结算失败原因
        web.ctx.session.failreason="pay"        

        total_num = i.get('total_num')
        # 2016/01/02 Start

        tminterval_type = i.get('tminterval_type')
        invoice_type = i.get('invoice_type')
        invoice = ""
        if invoice_type == "1":
            invoice = i.get('invoice')
        # End
        officeid  = web.ctx.session.officeid
        menu_date = web.ctx.session.menu_date
        
        routeid = web.cookies().get('routeid')
        #all_price = web.cookies().get('total_price')
        price0 = web.ctx.session.price0
        price1 = web.ctx.session.price1
        price2 = web.ctx.session.price2		
        all_price = float(price0)-float(price1)+float(price2)
        #print total_price
        all_cnt = 0


        lunches = model.get_menu(routeid,menu_date)
        
        for lunch in lunches:
            num = web.cookies().get(str(lunch.ID))
            #print num            
            try:
                if int(num)>0:                                        
                    #清除购物车 TODO
                    #web.setcookie(str(lunch.ID), '', expires=-1)                    
                    meal_it = model.get_meal_detail(lunch.ID,menu_date)
                    meal_dtl = list(meal_it)
                    #print '库存:'+str(meal_dtl[0].stock)
                    #print '购买:'+str(num)
                    if int(meal_dtl[0].stock) >= int(num):
                        #新增订单详情
                        model.new_detail(orderid,lunch.ID,num)                    
                        #库存修改
                        ret = model.upd_meal_sold(lunch.ID,menu_date,num)
                        #print 'upd_meal_sold return:'+str(ret)
                        if ret == -1:
                            web.ctx.session.failreason = "stock"
                            model.del_order(orderid)
                            model.del_detail(orderid)                          
                            for (k,v) in lidict.items():
                                model.upd_meal_sold(k,menu_date,-int(v))                            
                            return web.seeother('/carte_failed')
                        elif ret == 0:
                            #暂存已更新的库存信息
                            lidict[lunch.ID] = num
                    else:
                        web.ctx.session.failreason="stock"
                        model.del_order(orderid)
                        model.del_detail(orderid)
                        for (k,v) in lidict.items():
                            model.upd_meal_sold(k,menu_date,-int(v))
                        return web.seeother('/carte_failed')
            except ValueError:
                print "invalid num value"
            except TypeError:
                print "invalid num type"
        #payment = i.get('payment')
        #if payment=='cash':
        #    return web.seeother('/success')
        #elif payment=='wenxinpay':
        #    return web.seeother('/prepay')         
        #    oid = web.ctx.session.orderid
        #    model.del_order(oid)
        #    model.del_detail(oid)
        #    return web.seeother('/order_list')
        logging.info("[pay][uid:%s]", str(web.ctx.session.userid))
        return web.seeother('/prepay?orderid='+str(orderid))
'''
