#!/usr/bin/env python
#coding=utf8

"""
	작성자 : 문중현
	내용:
		Restful API Exception class 정의

"""

__author__ = 'mjhans'
from F3.util.rest.RestException.defineErrorMsg import *

##############################################################################
class RestfulException(Exception):
	""" ftRestfulException class """

	#=========================================================================
	def __init__(self, *args, **kwargs):
		err_msg = "(%s)"
		err_code = T_UNKNOWN
		if "err_msg" in kwargs:
			err_msg = "(%s)" % (kwargs['err_msg'])
		if "err_code" in kwargs:
			err_code = kwargs["err_code"]
		tmsg = "[errcode : 0x%02X],[errmsg : %s%s]" % (err_code, str(REST_ERROR_MSG[err_code]),err_msg)
		message = str(tmsg)
		print message
		Exception.__init__(*args, **kwargs)
		self.message = message

	#=========================================================================
	def __str__(self):
		return repr(self.message)
