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
        rest_id = 0
        return render.qulification(rest_id)