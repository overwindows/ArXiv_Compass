#!/usr/bin/env python
################################################################################
#
# Copyright (c) 2015 Baidu.com, Inc. All Rights Reserved
#
################################################################################
"""
This module provide...

Authors: wuchen(wuchen@baidu.com)
Date:    2015/08/05 17:23:06
"""
# -*- coding:utf-8 -*-

import web
import cgi
import os
import sys

from weixin import *


reload(sys)
sys.setdefaultencoding('utf-8')

# Maximum input we will accept when REQUEST_METHOD is POST
cgi.maxlen = 10 * 1024 * 1024

urls = ("/", "index",
        "/coming_soon", "coming_soon",
       "/webchat","weixin",
        )
globals_dict={}
render = web.template.render('templates', globals=globals_dict)
app = web.application(urls, globals())

class index:
    def GET(self):
	    return render.index()

class coming_soon(object):
    """
    index 
    """
    def GET(self):
        """
	get
        """        
        return render.coming_soon()

if __name__ == '__main__':
    app.run()
