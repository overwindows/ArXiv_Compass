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

# Qulification Page
class qulification:
    def GET(self):
        msg = None
        return render.qulification()