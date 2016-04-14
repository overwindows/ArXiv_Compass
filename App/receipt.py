#coding:utf-8

import os
import web
import model
import time
import datetime
import json
import sign
import urllib
import urllib2

from env import *

class receipt:
    def GET(self):
        shopping_list = web.ctx.session.shoppinglist
        user_info = web.ctx.session.userinfo
        #menu_date = web.ctx.session.menudate
        #route_id = web.ctx.session.routeid
        order_list = {}

        for oid in shopping_list:
            #i = web.input()
            model.update_order_1(oid,1)
            order = list(model.get_order(oid))

            date_time = datetime.datetime.strptime(str(order[0].OrderDate), '%Y-%m-%d')
            _date_time = str(order[0].OrderDate)
            order_list[_date_time] = {}
            weekday = model.get_chinese_weekday(date_time.weekday())
            # Notice-Start
            lunch_info = list(model.get_details_1(oid))
            meal_str = '\n'
            for l in lunch_info:
                if not order_list[_date_time].has_key(l.ID):
                    order_list[_date_time][l.ID] = {}
                order_list[_date_time][l.ID]["Name"] = l.Meal
                order_list[_date_time][l.ID]["Price"] = l.Price
                order_list[_date_time][l.ID]["Count"] = l.num   
                meal_str += l.Meal
                meal_str += str(l.num)
                meal_str += u'份'
                meal_str += '\n'
            meal_str_0 = meal_str.rstrip('\n')

            disp_tm = ""
            if str(order[0].tminterval) == "0":
                disp_tm = "12:00-12:20"
            elif str(order[0].tminterval) == "1":
                disp_tm = "12:20-12:40"
            elif str(order[0].tminterval) == "2":
                disp_tm = "12:40-13:00"
        '''
        weixin_url = 'https://api.weixin.qq.com/cgi-bin/token'
        weixin_payload = 'grant_type=client_credential&appid=wx9e8d00301079061b&secret=6021e0985185092b430c4182db3b3f62'
        data=urllib2.urlopen(weixin_url, weixin_payload).read()
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
        urlObj['data']['keyword2']['value'] = str(order[0].OrderDate)+" "+weekday+" "+disp_tm
        urlObj['data']['keyword2']['color'] = '#173177'
        urlObj['data']['keyword3']={}
        urlObj['data']['keyword3']['value'] = order[0].OfficeName+" "+order[0].orderaddr
        urlObj['data']['keyword3']['color'] = '#173177'
        urlObj['data']['remark']={}
        urlObj['data']['remark']['value'] = '感谢您的惠顾，祝用餐愉快。'
        urlObj['data']['remark']['color'] = '#173177'
        json_data = json.dumps(urlObj)
        data = urllib.quote_plus(str(json_data))
        res = urllib2.urlopen(send_url,data=json_data).read()
       '''
        return render.receipt(user_info, order_list)
        # Notice-End
        # return render.carte_succeed(order[0], weekday)
