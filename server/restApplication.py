#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'mjhans'

"""
	참고 : https://github.com/rancavil/tornado-rest

"""


import re
from tornado.web import Application
from tornado.wsgi import WSGIApplication
from F3.util.rest.RestException import RestfulAPIException


##############################################################################
def create_restful_app(iswsgi, hdls, **kwargs):

	_app = None
	try:
		if iswsgi:
			_app = restfulApplication(hdls, **kwargs)
		else:
			_app = WSGIRestfulApplication(hdls, **kwargs)
	except RestfulAPIException, msg:
		raise RestfulAPIException("")
	except Exception, msg:
		print msg

	return _app


##############################################################################
class restfulApplication(Application):

	""" Class to create Rest services in tornado web server """
	resource = None

	#=========================================================================
	def __init__(self, rest_handlers, resource=None, handlers=None, default_host="", transforms=None, **settings):
		restservices = []
		self.resource = resource
		for r in rest_handlers:
			svs = self._generateRestServices(r)
			restservices += svs
		if handlers != None:
			restservices += handlers
		Application.__init__(self, restservices, default_host, transforms, **settings)

	#=========================================================================
	def _generateRestServices(self,rest):
		svs = []
		paths = rest.get_paths()
		for p in paths:
			s = re.sub(r"(?<={)\w+}",".*",p).replace("{","")
			o = re.sub(r"(?<=<)\w+","",s).replace("<","").replace(">","").replace("&","").replace("?","")
			svs.append((o,rest,self.resource))

		return svs


##############################################################################
class WSGIRestfulApplication(WSGIApplication):

	""" Class to create WSGI Rest services in tornado web server """
	resource = None


	#=========================================================================
	def __init__(self, rest_handlers, resource=None, handlers=None, default_host="", **settings):
		restservices = []
		self.resource = resource
		for r in rest_handlers:
			svs = self._generateRestServices(r)
			restservices += svs
		if handlers != None:
			restservices += handlers
		WSGIApplication.__init__(self, restservices, default_host, **settings)


	#=========================================================================
	def _generateRestServices(self,rest):
		svs = []
		paths = rest.get_paths()
		for p in paths:
			s = re.sub(r"(?<={)\w+}",".*",p).replace("{","")
			o = re.sub(r"(?<=<)\w+","",s).replace("<","").replace(">","").replace("&","").replace("?","")
			svs.append((o,rest,self.resource))

		return svs