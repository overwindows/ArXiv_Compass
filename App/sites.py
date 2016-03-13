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
import logging

from env import render

class sites:
    def GET(self):
	    offices = model.get_offices_ex()
		return render.sites()
	    #return render.index(offices,uid,msgs,islogin,web.ctx.session.nickname,web.ctx.session.headimgurl)