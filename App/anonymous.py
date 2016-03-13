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

#Login Page
class anonymous:
    def GET(self):
        msg = None
        return render.anonymous()