import os
import web
import model
import time
import datetime
import json
import sign
import urllib
import logging

t_globals = {
    'datestr': web.datestr,
    'cookie': web.cookies,
    'mktime': time.mktime,
    'time': time,
}
render = web.template.render('templates', globals=t_globals)
web.config.debug = False
# print "[DEBUG][env.py]"
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S',
                    filename="../../logs/" + str(os.getpid()) + ".log",
                    filemode='w')
logging.info('initialize runtime environment.')
