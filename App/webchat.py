#coding:utf-8

import os
import web
import model
import time
import datetime
import json
import sign
import urllib

class webchat:
    def GET(self):
        #跳转首页地址
        url='http://w.zhunshikaifan.com/index'
        encode_url=urllib.urlencode({'redirect_uri':url})
        weixin_url='https://open.weixin.qq.com/connect/oauth2/authorize?appid=wx9e8d00301079061b' + \
        '&'+encode_url+'&response_type=code&scope=snsapi_userinfo&state=123#wechat_redirect'
        # print "[DEBUG] weixin:",weixin_url
        return web.seeother(weixin_url)


class webchat_order:
    def GET(self):
        url='http://w.zhunshikaifan.com/order_entry'
        encode_url=urllib.urlencode({'redirect_uri':url})
        weixin_url='https://open.weixin.qq.com/connect/oauth2/authorize?appid=wx9e8d00301079061b' + \
        '&'+encode_url+'&response_type=code&scope=snsapi_userinfo&state=123#wechat_redirect'
        return web.seeother(weixin_url)