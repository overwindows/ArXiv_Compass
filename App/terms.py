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

#用户协议
class terms:
    def GET(self):
        return render.terms()