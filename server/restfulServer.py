#!/usr/bin/env python
# -*- coding: utf-8 -*-


__author__ = 'mjhans'

from  tornado.ioloop import IOLoop
from tornado import gen
from tornado.httpserver import HTTPServer
from restApplication import create_restful_app
from F3.util.rest.RestException.RestfulAPIException import *
from F3.util.rest.server.logger import web_logger

##############################################################################
class http_server(object):

	#=========================================================================
	PORT = 8888
	PROCESS_NUM = 0 # all process
	HANDLERS = list()
	ISWSGI = False

	#=========================================================================
	def __init__(self, port=8888, process_num=0, handlers=[], wsgi=False):
		self.PORT = port
		self.PROCESS_NUM = process_num
		self.HANDLERS = handlers
		self.ISWSGI = wsgi
		self.logger = web_logger()

	#=========================================================================
	def start(self):
		try:

			app = create_restful_app(self.ISWSGI, self.HANDLERS)
			server = HTTPServer(app)
			server.bind(self.PORT)
			self.logger.info("Port: %s, process count: %s" % (self.PORT, self.PROCESS_NUM))
			server.start(self.PROCESS_NUM)
			IOLoop.current().start()

		except Exception, msg:
			raise RestfulException(err_code=T_START_ERROR, err_msg=msg)
