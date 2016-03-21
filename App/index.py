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
        # 初始化送餐楼宇编号
        web.ctx.session.routeid = 0
        web.ctx.session.officeid = 0
        
        # initialize menu dates
        current_day = datetime.date.today()
        current_wkday = int(current_day.weekday())
        menu_dates = list(model.get_menu_dates(current_day))
        menu_calendar = {}        
        for menu_date in menu_dates:
            _date = datetime.datetime.strptime(str(menu_date.sche_date), "%Y-%m-%d").date()
            menu_calendar[str(menu_date.sche_date)] = model.get_chinese_weekday(_date.weekday())         
        web.ctx.session.menucalendar = menu_calendar
        
        # initialize shopping basket
        shopping_basket={}
        web.ctx.session.shoppingbasket = shopping_basket
        
        # initialize user info
        user_info = {}
        web.ctx.session.userinfo = user_info

        
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
        try:
            user_iter=model.get_user_1(web.ctx.session.openid)
            user = list(user_iter)
        except AttributeError:
            web.ctx.session.nickname = "亲"
            web.ctx.session.headimgurl = "../static/img/img_18.png"
            user = None
        msgs = []
        # print "[DEBUG] Get UserInfo in OnTimeReal"
        if user:
            web.ctx.session.userid = user[0].id
            web.setcookie('userid', user[0].id, 3600)
            # 用于在点餐页结算时判断是否登录
            web.setcookie('username', user[0].username, 3600)
            web.setcookie('contactname', user[0].contactname, 3600)
            web.setcookie('unitaddress', user[0].unitaddress, 3600)
            msgs_it = model.ongoing_orders_cnt(user[0].id)
            msgs = list(msgs_it)
            web.ctx.session.officeid = user[0].officeid
            #session.msgs = msgs
        # print "[DEBUG] Prepare Date"        
        today = datetime.date.today()
        weekday_today = today.weekday()
        # print weekday_today
        tomorrow = today + datetime.timedelta(days=1)
        weekday_tomorrow = tomorrow.weekday()
        # print weekday_tomorrow
        # print os.getcwd()
        # offices = model.get_offices()
        # web.setcookie('url', "/index?code=Fake", 3600)
        
        #日期初始化
        web.ctx.session.today = str(today)
        web.ctx.session.tomorrow = str(tomorrow)
        web.ctx.session.weekday_today = int(weekday_today)
        web.ctx.session.weekday_tomorrow = int(weekday_tomorrow)
        
        islogin = 0        
        #username = ""
        uid = ""
        try:
            #if session.username:
            if web.ctx.session.userid:
                islogin = 1
                #username = session.username
                uid = web.ctx.session.userid
            else:
                islogin = 0
        except AttributeError:
                islogin = 0
        #logging.info("[office][uid:%s]", uid)
        if int(web.ctx.session.officeid)==0:
            return web.seeother("/sites")
        else:
            #return web.seeother("carte_index/0?office_id=" + str(web.ctx.session.officeid))
            return web.seeother("/menus")
