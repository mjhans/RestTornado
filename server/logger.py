#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'mjhans'


import os
import logging
import logging.handlers
import threading
from define import *


##############################################################################
class web_logger(object):
	"""
		restful server 로깅담당
		debug, info, warning, error, critical 함수 지원

		생성시
		{
			"log_name" : [str],
			"log_level" : [int]
		}
	"""
	logger = None
	LOGDIR = None
	LOGFILE = ""
	NAME = None


	#=========================================================================
	def __init__(self, **kwargs):

		self.LOGDIR = os.getenv("REST_LOG")
		if "REST_LOG" in kwargs:
			self.LOGDIR = kwargs["REST_LOG"]

		print "log dir : %s" % self.LOGDIR
		if self.LOGDIR in ["", None]:
			self.LOGDIR = DEFAULT_LOG_PATH

		if not os.path.exists(self.LOGDIR):
			os.makedirs(self.LOGDIR)

		self.NAME = LOG_NAME

		if "verbose" in kwargs:
			self.verbose = kwargs["verbose"]
		else:
			self.verbose = True

		if "log_name" in kwargs:
			self.NAME = kwargs["log_name"]

		# set log
		self.logger = logging.getLogger(self.NAME)

		# set log level
		if "log_level" in kwargs:
			self.logger.setLevel(kwargs["log_level"])
		else:
			self.logger.setLevel(LOG_LV_INFO)

		# set log file name
		self.LOGFILE="%s/%s.log" % (self.LOGDIR, self.NAME)

		# set handler
		# 1. remove handler
		if self.logger.handlers is not None and len(self.logger.handlers) >= 0:
			for hdls in self.logger.handlers:
				self.logger.removeHandler(hdls)
			self.logger.handlers = []

		# 2. set rotating handler
		log_hdls = logging.handlers.RotatingFileHandler(
			self.LOGFILE, maxBytes=LOG_SIZE, backupCount=LOG_BACKUP_CNT
		)

		# 3. set log formatter
		log_frmt = logging.Formatter('%(asctime)s-%(name)s-%(levelname)s-%(message)s')
		log_hdls.setFormatter(log_frmt)

		# 4. set log handler
		self.logger.addHandler(log_hdls)
		pass

	#=========================================================================
	def debug(self, msg):
		cur_tid = str(threading.current_thread().getName())
		frm_msg = ('[%s:%s] %s') % (os.getpid(), cur_tid, msg)
		if self.verbose:
			print frm_msg
		self.logger.debug(frm_msg)

	#=========================================================================
	def info(self, msg):
		cur_tid = str(threading.current_thread().getName())
		frm_msg = ('[%s:%s] %s') % (os.getpid(), cur_tid, msg)
		if self.verbose:
			print frm_msg
		self.logger.info(frm_msg)

	#=========================================================================
	def warning(self, msg):
		cur_tid = str(threading.current_thread().getName())
		frm_msg = ('[%s:%s] %s') % (os.getpid(), cur_tid, msg)
		if self.verbose:
			print frm_msg
		self.logger.warning(frm_msg)

	#=========================================================================
	def error(self, msg):
		cur_tid = str(threading.current_thread().getName())
		frm_msg = ('[%s:%s] %s') % (os.getpid(), cur_tid, msg)
		if self.verbose:
			print frm_msg
		self.logger.error(frm_msg)

	#=========================================================================
	def critical(self, msg):
		cur_tid = str(threading.current_thread().getName())
		frm_msg = ('[%s:%s] %s') % (os.getpid(), cur_tid, msg)
		if self.verbose:
			print frm_msg
		self.logger.critical(frm_msg)


