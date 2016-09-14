#!/usr/bin/env python
#coding=utf8

#################################################################################
#
#       tornado server test
#
#################################################################################

__author__ = 'mjhans'

from F3.util.rest.server.restfulServer import http_server
from F3.util.rest.server.types import *
from F3.util.rest.server.restfulAPI import *

class testHandler(BaseRequestHandler):

	people = {
		"age" : 0,
		"name" : "test"
	}
	@get(_path="/hello/test")
	def writeTest(self):
		print "get"
		return self.people

	@post(_path="/hello/test")
	def writeTest2(self):
		print "post"
		return self.people

	@put(_path="/hello/test")
	def writeTest3(self):
		print "put"
		return self.people

	@delete(_path="/hello/test")
	def writeTest4(self):
		print "delete"
		return self.people

	@get(_path="/hello/test2")
	@post(_path="/hello/test2")
	def writeTest5(self):
		print "get,post"
		print self.request.arguments
		print self.get_argument("a")
		return self.people

if __name__ == "__main__":
	try:
		reqhandlers = [
			testHandler
		]
		server = http_server(port=8888, process_num=3, handlers=reqhandlers)
		server.start()
	except Exception, msg:
		print msg
