#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'mjhans'

"""
	https://github.com/rancavil/tornado-rest

	주고 받는 데이터는 무조건 json과 dict로 한다
"""

import inspect
import re
from restfulMediatype import *
from define import *
from types import convert
from F3.util.rest.RestException.RestfulAPIException import RestfulException
from tornado.web import RequestHandler, HTTPError
from tornado import gen
import xml.dom.minidom
from json import dumps, loads


#=========================================================================
def config(func, method, **kwparams):
	""" Decorator config function """
	path = "/"
	types = None
	media_type = None
	_callback = None
	_async = False

	if len(kwparams):
		path = kwparams['_path']
		if '_types' in kwparams:
			types = kwparams['_types']

		if "_callback" in kwparams:
			_callback = kwparams["_callback"]
			_async = True


		if "_media" in kwparams:
			media_type = kwparams['_media']
		else:
			media_type = APPLICATION_JSON

	def operation(*args,**kwargs):
		return func(*args,**kwargs)

	operation.func_name = func.__name__
	operation._func_params = inspect.getargspec(func).args[1:]
	operation._types = types
	operation._service_name = re.findall(r"(?<=/)\w+",path)
	operation._method = method
	operation._media_type = media_type
	operation._path  = path
	operation._async = _async
	operation._callback = _callback


	if not operation._media_type in [APPLICATION_JSON, APPLICATION_XML,TEXT_XML, None]:
		raise RestfulException("The media type used do not exist : "+ operation.func_name)

	return operation

#=========================================================================
def get(*params, **kwparams):
	""" Decorator for config a python function like a Rest GET verb	"""
	def method(f):
		return config(f,'GET',**kwparams)
	return method

#=========================================================================
def post(*params, **kwparams):
	""" Decorator for config a python function like a Rest POST verb	"""
	def method(f):
		return config(f,'POST',**kwparams)
	return method


#=========================================================================
def put(*params, **kwparams):
	""" Decorator for config a python function like a Rest PUT verb	"""
	def method(f):
		return config(f,'PUT',**kwparams)
	return method


#=========================================================================
def delete(*params, **kwparams):
	""" Decorator for config a python function like a Rest PUT verb	"""
	def method(f):
		return config(f,'DELETE',**kwparams)
	return method


##############################################################################
class BaseRequestHandler(RequestHandler):


	#=========================================================================
	def get(self):
		""" Executes get method """
		self._exe('GET')

	#=========================================================================
	def post(self):
		""" Executes post method """
		self._exe('POST')

	#=========================================================================
	def put(self):
		""" Executes put method"""
		self._exe('PUT')

	#=========================================================================
	def delete(self):
		""" Executes put method"""
		self._exe('DELETE')

	#=========================================================================
	def _exe(self, method):
		"""
			Executes the python function for the Rest Service
			only dict....
		"""

		request_path = self.request.path
		path = request_path.split('/')
		services_and_params = list(filter(lambda x: x!='',path))

		content_type = None
		if 'Content-Type' in self.request.headers.keys():
			content_type = self.request.headers['Content-Type']

		# Get all funcion names configured in the class RestHandler
		functions    = list(filter(lambda op: hasattr(getattr(self,op),'_service_name') == True and inspect.ismethod(getattr(self,op)) == True, dir(self)))
		# Get all http methods configured in the class RestHandler
		#http_methods = list(map(lambda op: getattr(getattr(self,op),'_method'), functions))
		#print "http method : %s" % http_methods
		#http_methods = ["PUT", "GET","POST","DELETE"]

		if method not in HTTP_METHODS:
			raise HTTPError(405,'The service not have %s verb'%method)

		for operation in list(map(lambda op: getattr(self,op), functions)):
			service_name = getattr(operation,"_service_name")
			media_type = getattr(operation,"_media_type")
			services_from_request = list(filter(lambda x: x in path,service_name))

			if operation._method == self.request.method and service_name == services_from_request:
				try:
					self.set_header("Content-Type",media_type)

					response = operation()
					print "response : %s"% response

					if media_type == APPLICATION_JSON and isinstance(response,dict):
						self.write(response)
						self.finish()
					elif media_type == APPLICATION_JSON and isinstance(response,list):
						self.write(dumps(response))
						self.finish()
					elif media_type in [APPLICATION_XML, TEXT_XML] and isinstance(response,xml.dom.minidom.Document):
						self.write(response.toxml())
						self.finish()
					else:
						self.gen_http_error(500,"Internal Server Error : response is not %s document"% media_type)
				except Exception as detail:
					self.gen_http_error(500,"Internal Server Error : %s"%detail)

	#=========================================================================
	def _find_params_value_of_url(self,services,url):
		""" Find the values of path params """
		values_of_query = list()
		i = 0
		url_split = url.split("/")
		values = [item for item in url_split if item not in services and item != '']
		for v in values:
			if v != None:
				values_of_query.append(v)
				i+=1
		return values_of_query

	#=========================================================================
	def _find_params_value_of_arguments(self, operation):
		values = []
		if len(self.request.arguments) > 0:
			a = operation._service_params
			b = operation._func_params
			params = [item for item in b if item not in a]
			for p in params:
				if p in self.request.arguments.keys():
					v = self.request.arguments[p]
					values.append(v[0])
				else:
					values.append(None)
		elif len(self.request.arguments) == 0 and len(operation._query_params) > 0:
			values = [None]*(len(operation._func_params) - len(operation._service_params))
		return values

	#=========================================================================
	def _convert_params_values(self, values_list, params_types):
		""" Converts the values to the specifics types """
		values = list()
		i = 0
		for v in values_list:
			if v != None:
				values.append(convert(v,params_types[i]))
			else:
				values.append(v)
			i+=1
		return values

	#=========================================================================
	def gen_http_error(self,status,msg):
		""" Generates the custom HTTP error """
		self.clear()
		self.set_status(status)
		self.write("<html><body>"+str(msg)+"</body></html>")
		self.finish()

	#=========================================================================
	@classmethod
	def get_services(self):
		""" Generates the resources (uri) to deploy the Rest Services """
		services = []
		for f in dir(self):
			o = getattr(self,f)
			if callable(o) and hasattr(o,'_service_name'):
				services.append(getattr(o,'_service_name'))
		return services

	#=========================================================================
	@classmethod
	def get_paths(self):
		""" Generates the resources from path (uri) to deploy the Rest Services """
		paths = []
		for f in dir(self):
			o = getattr(self,f)
			if callable(o) and hasattr(o,'_path'):
				paths.append(getattr(o,'_path'))
		return paths

	#=========================================================================
	@classmethod
	def get_handlers(self):
		""" Gets a list with (path, handler) """
		svs = []
		paths = self.get_paths()
		for p in paths:
			s = re.sub(r"(?<={)\w+}",".*",p).replace("{","")
			o = re.sub(r"(?<=<)\w+","",s).replace("<","").replace(">","").replace("&","").replace("?","")
			svs.append((o,self))

		return svs


##############################################################################
class BaseRequestAsyncHandler(BaseRequestHandler):

	#=========================================================================
	@gen.coroutine
	def get(self):
		""" Executes get method """
		self._exe('GET')

	#=========================================================================
	@gen.coroutine
	def post(self):
		""" Executes post method """
		self._exe('POST')

	#=========================================================================
	@gen.coroutine
	def put(self):
		""" Executes put method"""
		self._exe('PUT')

	#=========================================================================
	@gen.coroutine
	def delete(self):
		""" Executes put method"""
		self._exe('DELETE')
