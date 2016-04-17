#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os
import web
import model
import time
import datetime
import json
import urllib
import random
import urllib2

from env import *

class orderfail:
    def GET(self):
        #浏览器回退防御
        if web.ctx.session.failreason=="expired":
            return render.orderfail(None,web.ctx.session.failreason)
        #model.update_order_1(oid,0)
        if web.ctx.session.failreason == "pay" :
            oid = web.ctx.session.pay_oid
            order = list(model.get_order(oid))
            '''
            # Notice-Start
            date_time = datetime.datetime.strptime(str(order[0].OrderDate),'%Y-%m-%d')
            lunch_info = list(model.get_details_1(oid))
            meal_str = '\n'
            for l in lunch_info:
                meal_str += l.Meal
                meal_str += str(l.num)
                meal_str += u'份'
                meal_str += '\n'
            meal_str_0 = meal_str.rstrip('\n')

            weixin_url = 'https://api.weixin.qq.com/cgi-bin/token'
            weixin_payload = 'grant_type=client_credential&appid=wx9e8d00301079061b&secret=6021e0985185092b430c4182db3b3f62'
            data = urllib2.urlopen(weixin_url, weixin_payload).read()
            weixin_access_token=json.loads(data)['access_token']
            send_url = 'https://api.weixin.qq.com/cgi-bin/message/template/send?access_token='+weixin_access_token
            urlObj = {}
            urlObj['touser'] = web.ctx.session.openid
            urlObj['template_id']='OBRKVZrD68qGejXB1ujq2OcZ1Rg2zHIKhqumF-l6UyM'
            #urlObj['url']='www.zhunshikaifan.com'
            urlObj['data']={}
            urlObj['data']['first']={}
            urlObj['data']['first']['value'] = '您好，你的午餐下单成功'
            urlObj['data']['first']['color'] = '#173177'
            urlObj['data']['keyword1'] = {}
            urlObj['data']['keyword1']['value'] = meal_str_0
            urlObj['data']['keyword1']['color'] = '#173177'
            urlObj['data']['keyword2']={}
            urlObj['data']['keyword2']['value'] = str(date_time)
            urlObj['data']['keyword2']['color'] = '#173177'
            urlObj['data']['keyword3']={}
            urlObj['data']['keyword3']['value'] = order[0].OfficeName+" "+order[0].OfficePlace
            urlObj['data']['keyword3']['color'] = '#173177'
            urlObj['data']['remark']={}
            urlObj['data']['remark']['value']='感谢您的惠顾，祝用餐愉快。'
            urlObj['data']['remark']['color']='#173177'
            json_data = json.dumps(urlObj)
            data = urllib.quote_plus(str(json_data))
            res = urllib2.urlopen(send_url,data=json_data).read()
            # Notice-End
            '''
            return render.orderfail(order[0],web.ctx.session.failreason)
        elif web.ctx.session.failreason=="stock":
            return render.orderfail(None,web.ctx.session.failreason)
