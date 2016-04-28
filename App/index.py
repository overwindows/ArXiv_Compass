#coding:utf-8

import os
import web
import model
import time
import datetime
import json
import sign
import urllib

from env import render

class index:
    def GET(self):
        i = web.input()
        web.ctx.session.openid = i.openid
        web.ctx.session.nickname = i.nickname
        web.ctx.session.headimgurl = i.headimgurl

        # 初始化送餐楼宇编号
        web.ctx.session.routeid = 0
        web.ctx.session.officeid = 0

        # initialize menu dates
        current_day = datetime.date.today()
        web.ctx.session.menudate = str(current_day)
        #current_wkday = int(current_day.weekday())

        # check if today's menu overtime
        ot_ts  = int(time.mktime(time.strptime(str(current_day) + " 10:30:00", "%Y-%m-%d %H:%M:%S")))
        cur_ts = int(time.time())
        if cur_ts > ot_ts:
            current_day = current_day + datetime.timedelta(days=1)
            menu_dates = list(model.get_menu_dates(current_day))
        else:
            menu_dates = list(model.get_menu_dates(current_day))

        menu_calendar = {}        
        for menu_date in menu_dates:
            _date = datetime.datetime.strptime(str(menu_date.sche_date), "%Y-%m-%d").date()
            menu_calendar[str(menu_date.sche_date)] = model.get_chinese_weekday(_date.weekday())         

        web.ctx.session.menucalendar = menu_calendar

        # initialize shopping basket
        shopping_basket = {}
        web.ctx.session.shoppingbasket = shopping_basket

        shopping_cost = {}
        web.ctx.session.shoppingcost = shopping_cost

        shopping_list = []
        web.ctx.session.shoppinglist = shopping_list

        web.ctx.session.redirecturl = None

        # initialize user info
        try:
            if web.ctx.session.userinfo:
                user_info = web.ctx.session.userinfo
            else:
                user_info = {}
                web.ctx.session.userinfo = user_info
        except AttributeError:
            user_info = {}
            web.ctx.session.userinfo = user_info

        # initialize price
        shopping_cost = {}
        web.ctx.session.shoppingcost = shopping_cost

        # 2016/04/17
        web.ctx.session.failreason = "pay"

        # 2016/04/29
        web.ctx.session.webpage = "index"
        #
        '''
        i = web.input()
        # CODE from WebChat
        #print "[DEBUG] Get Code:"+CODE
        webchat_code = i.get("code")
        if webchat_code:           
            web.ctx.session.code = webchat_code
            #print "[DEBUG] Get AccessToken and OpenID"			
            weixin_url='https://api.weixin.qq.com/sns/oauth2/access_token'
            weixin_payload='appid=wx9e8d00301079061b&secret=6021e0985185092b430c4182db3b3f62&code='+ \
            webchat_code+'&grant_type=authorization_code'
            data=urllib2.urlopen(weixin_url, weixin_payload).read()            
            #print data
            weixin_openid=json.loads(data)['openid']
            weixin_access_token=json.loads(data)['access_token']
            weixin_refresh_token=json.loads(data)['refresh_token']
            #https://api.weixin.qq.com/sns/userinfo?access_token=ACCESS_TOKEN&openid=OPENID&lang=zh_CN
            #print "[DEBUG] Get UserInfo in WebChat"
            usrinf_url='https://api.weixin.qq.com/sns/userinfo'
            usrinf_payload='access_token='+weixin_access_token+'&openid='+weixin_openid+'&lang=zh_CN'
            #print usrinf_payload
            data=urllib2.urlopen(usrinf_url, usrinf_payload).read()
            #print data
            web.ctx.session.openid = weixin_openid
            web.ctx.session.nickname=json.loads(data)['nickname']
            web.ctx.session.headimgurl=json.loads(data)['headimgurl']            
        #print session.openid
        #print session.nickname
        '''
        user_iter=model.get_user_1(web.ctx.session.openid)
        user = list(user_iter)

        if user:
            user_info['ID'] = user[0].id
            user_info['Name'] = user[0].username
            user_info['Contact'] = user[0].contactname
            user_info['Tel'] = user[0].tel
            user_info['UnitAddr'] = user[0].unitaddress
            user_info['Invoice'] = ""

            web.ctx.session.officeid = user[0].officeid
            #msgs_it = model.ongoing_orders_cnt(user[0].id)
            #msgs = list(msgs_it)
            #session.msgs = msgs

        # print os.getcwd()
        # offices = model.get_offices()
        #logging.info("[office][uid:%s]", uid)
        if web.ctx.session.officeid:
            return web.seeother("/menus")
        else:
            return web.seeother("/sites")
