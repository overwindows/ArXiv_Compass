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
        i = web.input()
        office_id = i.get("officeid")        
        menu_date = i.get("menudate")
        route_id  = i.get("routeid")  
        lunches_info = {}
        menu_calendar = web.ctx.session.menucalendar
        shopping_basket = web.ctx.session.shoppingbasket
        user_info = web.ctx.session.userinfo
        
        # guard code
        if menu_date is None:            
            key_list = menu_calendar.keys()
            menu_date = key_list[0]

        if route_id is None:
            route_id = 0
            
        lunches = model.get_menu(int(route_id), menu_date)

        web.ctx.session.officeid = office_id
        web.ctx.session.menudate = menu_date

        offices_iter = model.get_office(int(office_id))
        offices = list(offices_iter)
        user_info["OfficeAddr"] = offices[0].Name
        
        if shopping_basket.has_key(menu_date):
            lunches_info = shopping_basket[menu_date]


        web.ctx.session.userinfo = user_info

        return render.menus(menu_calendar, lunches, offices[0], menu_date, lunches_info)
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
        
        ot_ts  = int(time.mktime(time.strptime(str(menu_date)+" 10:30:00", "%Y-%m-%d %H:%M:%S")))
        cur_ts = int(time.time())
        if cur_ts > ot_ts:
            OT=True
        else:
            OT=False
        
        lunches_list = list(lunches)
        #清空原有购物车内容(本日)
        for lunch in lunches_list:            
            web.setcookie(str(lunch.ID), 0, expires=-1)
        logging.info("[menu][uid:%s]", uid)
        return render.carte_index(lunches_list, route_id,office[0].officeid,office[0].Name,office[0].Address,today,tomorrow,islogin,uid,\
                                  msgs,menu_date,OT,web.ctx.session.nickname, web.ctx.session.headimgurl, \
                                  model.get_chinese_weekday(web.ctx.session.weekday_today), model.get_chinese_weekday(web.ctx.session.weekday_tomorrow))   
    '''
