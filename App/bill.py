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

#下单结账
class bill:
    def GET(self):
        shopping_basket = web.ctx.session.shoppingbasket
        shopping_cost  = web.ctx.session.shoppingcost
        user_info = web.ctx.session.userinfo
        menu_date = web.ctx.session.menudate
        route_id = web.ctx.session.routeid
        menu_calendar = web.ctx.session.menucalendar

        i = web.input()
        param = i.get("param")
        if param:
            order_info = {}
            order_list = param.split("|")
            for order in order_list:
                if order:
                    id,cnt = order.split("_")
                    order_info[id] = cnt
            lunches = list(model.get_menu(int(route_id), menu_date))
            for lunch in lunches:
                if order_info.has_key(lunch.ID):
                    cnt = order_info[lunch.ID]
                    if not shopping_basket.has_key(menu_date):
                        shopping_basket[menu_date] = {}
                    if not shopping_basket[menu_date].has_key(lunch.ID):
                        shopping_basket[menu_date][lunch.ID] = {}
                    shopping_basket[menu_date][lunch.ID]["Count"] = cnt
                    shopping_basket[menu_date][lunch.ID]["Price"] = lunch.Price
                    shopping_basket[menu_date][lunch.ID]["Name"] = lunch.Meal

                    if not shopping_cost.has_key(menu_date):
                        shopping_cost[menu_date] = {}
                    shopping_cost[menu_date]["price0"] = float(lunch.Price) * float(cnt)
                    shopping_cost[menu_date]["price1"] = 0
                    shopping_cost[menu_date]["price2"] = 0
                    shopping_cost[menu_date]["price"] = shopping_cost[menu_date]["price0"]

            web.ctx.session.shoppingbasket = shopping_basket
            web.ctx.session.shoppingcost = shopping_cost

        # print shopping_basket.keys()

        if user_info.has_key("ID"):
            return render.bill(user_info, shopping_basket, menu_calendar)
        else:
            web.ctx.session.redirecturl = "/bill"
            web.seeother('/login')   
	'''
        #浏览器回退防御
        if web.ctx.session.webbrowser_backstep == "danger":
            web.ctx.session.failreason = "expired"            
            return web.seeother('/carte_failed')
        elif web.ctx.session.webbrowser_backstep == "safe":
            web.ctx.session.webbrowser_backstep = "danger"
        
        i = web.input()
        shopping_basket_num = {}
        shopping_basket_price = {}
        shopping_basket_name = {}
        order_type = 0
        menu_date = i.menu_date
        print menu_date
        web.ctx.session.menu_date = menu_date       
        # if i:
        #    orderid = i.id
        #    session.orderid = orderid
        #    details = model.get_details(int(orderid))
        #    for detail in details:
        #        l_iter = model.get_lunch(int(detail.lunchid))
        #        l = list(l_iter)
        #        shopping_basket_num[detail.lunchid] = detail.num
        #        shopping_basket_price[detail.lunchid] = l[0].Price
        #        shopping_basket_name[detail.lunchid] = l[0].Meal
        #    order_type = 1    
        #    return render.carte_detail(shopping_basket_num,shopping_basket_price,shopping_basket_name,order_type)
        #else:            
        route_id  = web.cookies().get('routeid')
        office_id = web.cookies().get('officeid')
        office_info = list(model.get_office(office_id))
        unit_addr = office_info[0].place
        web.ctx.session.price0 = web.cookies().get('total_price')
        
        #[2015/11/28] 12.1活动方案
        favor_type = 0
        
        #res_order_cnt = list(model.get_user_orders_cnt(web.ctx.session.userid,'2015-12-01'))
        res_order_cnt = 1
        		
        rec_cnt = res_order_cnt[0].cnt
        t1 = time.strptime(menu_date, "%Y-%m-%d")
        t2 = time.strptime('2015-12-01', "%Y-%m-%d")
        #print rec_cnt
        #套餐运费
        web.ctx.session.price2 = 5
        if int(rec_cnt) == 0 and t1 >= t2:
            # print "注册后首单减免策略"
            favor_type = 1            
            if int(web.ctx.session.price0) >= 99:
                web.ctx.session.price1 = 50
            elif int(web.ctx.session.price0) >= 20:
                web.ctx.session.price1 = 20
            else:
                web.ctx.session.price1 = web.ctx.session.price0
        else:
            # print "非首单减免策略"            
            if int(web.ctx.session.price0)/25 > 0 and t1 < t2:
                favor_type = 2
                web.ctx.session.price1 = 8
            else:
                web.ctx.session.price1 = 0
                if menu_date != web.ctx.session.today:
                    favor_type = 3
                    #早鸟计划
                    web.ctx.session.price2 = 0
        
        #web.ctx.session.price1 = (int(web.ctx.session.price0)/25)*8
		
        lunches = model.get_menu(int(route_id),menu_date)
        for lunch in lunches:
            num = web.cookies().get(str(lunch.ID))
            try:            
                if int(num)>0:
                    shopping_basket_num[lunch.ID]=num
                    shopping_basket_price[lunch.ID]=lunch.Price
                    shopping_basket_name[lunch.ID]=lunch.Meal
            except ValueError:
                print "invalid num value"
            except TypeError:
                print "invalid num type"
                    
        web.setcookie('url', 'check_order', 3600)
        order_type = 0
        logging.info("[bill][uid:%s]", str(web.ctx.session.userid))
        return render.carte_detail(shopping_basket_num,shopping_basket_price,shopping_basket_name,order_type,route_id,office_id, \
            menu_date, web.ctx.session.price0,web.ctx.session.price1,web.ctx.session.price2,favor_type,unit_addr)
    '''
