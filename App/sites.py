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
        #offices = model.get_offices_ex()
         
        districts = list(model.get_districts())
        zones = list(model.get_zones())
        plazas = list(model.get_plazas())
        offices = list(model.get_offices_ex())

        # clear shopping_basket and shopping cost
        if web.ctx.session.shoppingbasket:
            web.ctx.session.shoppingbasket.clear()
        if web.ctx.session.shoppingcost:
            web.ctx.session.shoppingcost.clear()
           
        return render.sites(districts, zones, plazas, offices)
        #return render.index(offices,uid,msgs,islogin,web.ctx.session.nickname,web.ctx.session.headimgurl)
