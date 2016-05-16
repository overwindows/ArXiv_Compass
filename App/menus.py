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

#菜单
class menus:
    def GET(self):
       
        # 2016/04/29 guard code.  
        if web.ctx.session.webpage=="bill":
            web.ctx.session.webpage="menus"
            return web.seeother("menus")

        i = web.input()
        office_id = i.get("officeid")        
        menu_date = i.get("menudate") # different meaning, NEXT menudate
        route_id  = i.get("routeid")  

        if route_id is None:
            route_id = 0
        
        lunches_info = {}
        menu_calendar = web.ctx.session.menucalendar
        shopping_basket = web.ctx.session.shoppingbasket
        shopping_cost = web.ctx.session.shoppingcost
        shopping_discount = web.ctx.session.shoppingdiscount
        user_info = web.ctx.session.userinfo
        
        #if parameters, load previous menu date
        param = i.get("param")
        if param:
            _menudate = web.ctx.session.menudate
            order_info = {}
            # print _menudate+":"+param 
            order_list = param.split("|")
            for order in order_list:
                if order:
                    id,cnt = order.split("_")
                    order_info[id] = cnt
            lunches = list(model.get_menu(int(route_id), _menudate))

            _count = 0
            _price0 = 0.0
            _price2 = 5.0

            if _menudate != str(datetime.date.today()):
                shopping_discount[_menudate] = 1 #早鸟计划

            for lunch in lunches:
                if order_info.has_key(lunch.ID):
                    cnt = order_info[lunch.ID]
                    if not shopping_basket.has_key(_menudate):
                        shopping_basket[_menudate] = {}
                    if not shopping_basket[_menudate].has_key(lunch.ID):
                        shopping_basket[_menudate][lunch.ID] = {}
                    shopping_basket[_menudate][lunch.ID]["Count"] = cnt
                    shopping_basket[_menudate][lunch.ID]["Price"] = lunch.Price
                    shopping_basket[_menudate][lunch.ID]["Name"] = lunch.Meal

                    _price0 += float(lunch.Price) * float(cnt)
                    _count  += int(cnt)
                else:
                    if shopping_basket.has_key(_menudate) and shopping_basket[_menudate].has_key(lunch.ID):
                        del shopping_basket[_menudate][lunch.ID]

            if not shopping_cost.has_key(_menudate):
                shopping_cost[_menudate] = {}
            shopping_cost[_menudate]["price0"] = _price0
            shopping_cost[_menudate]["price"] = _price0 + _price2
            shopping_cost[_menudate]["price2"] = _price2
            shopping_cost[_menudate]["price1"] = 0
            shopping_cost[_menudate]["count"] = _count

            web.ctx.session.shoppingbasket = shopping_basket
            web.ctx.session.shoppingcost   = shopping_cost
            web.ctx.session.shoppingdiscount = shopping_discount

        # guard code
        menu_calender_sorted = sorted(menu_calendar.items(), key=lambda menu_calendar:menu_calendar[0])
        if menu_date is None:
            menu_date = menu_calender_sorted[0][0]
        # print menu_date
        
        if office_id is None:
           office_id = web.ctx.session.officeid
            
        lunches = model.get_menu(int(route_id), menu_date)

        web.ctx.session.officeid = office_id

        offices_iter = model.get_office(int(office_id))
        offices = list(offices_iter)
        user_info["OfficeAddr"] = offices[0].Name
        user_info["OfficeId"] = office_id
        
        if shopping_basket.has_key(str(menu_date)):
            lunches_info = shopping_basket[str(menu_date)]

        web.ctx.session.userinfo = user_info

        # calculate shopping counts
        shopping_count = 0
        for _d in shopping_cost:
            if shopping_cost[_d].has_key("count"):
                shopping_count += shopping_cost[_d]["count"]

        web.ctx.session.menudate = str(menu_date)
        web.ctx.session.webpage = "menus"
        return render.menus(menu_calender_sorted, lunches, offices[0], menu_date, lunches_info, shopping_count)
	'''
        #backstep = int(web.cookies().get('backstep')) 
        #浏览器回退防御
        web.ctx.session.webbrowser_backstep = "safe";
        print "[DEBUG] Get Menu Date"  
        today = web.ctx.session.today
        tomorrow = web.ctx.session.tomorrow

        islogin=0
        msgs = [] 
        try:
            if web.ctx.session.userid:
                islogin = 1
                uid = web.ctx.session.userid
                msgs_it = model.ongoing_orders_cnt(uid)
                msgs = list(msgs_it)
            else:
                islogin = 0
                uid=""
        except AttributeError:
                islogin = 0
                uid=""                
        
        web.setcookie('menudate',menu_date, 3600)
        web.setcookie('url','/carte_detail?menu_date='+menu_date, 3600)
        web.setcookie('routeid',route_id, 3600)
        web.setcookie('officeid',office[0].officeid,3600)
        web.setcookie('officeaddress',office[0].Address,3600)
        web.setcookie('officename' , office[0].Name , 3600)
        web.setcookie('backstep',-1,3600)

        lunches_list = list(lunches)
        #清空原有购物车内容(本日)
        for lunch in lunches_list:            
            web.setcookie(str(lunch.ID), 0, expires=-1)
        logging.info("[menu][uid:%s]", uid)
        return render.carte_index(lunches_list, route_id,office[0].officeid,office[0].Name,office[0].Address,today,tomorrow,islogin,uid,\
                                  msgs,menu_date,OT,web.ctx.session.nickname, web.ctx.session.headimgurl, \
                                  model.get_chinese_weekday(web.ctx.session.weekday_today), model.get_chinese_weekday(web.ctx.session.weekday_tomorrow))   
    '''
