#!/usr/bin/env python
# -*- coding: utf-8 -*-


__author__ = 'mjhans'



HTTP_METHODS = ["PUT", "GET","POST","DELETE"]

LOG_LV_DEBUG = 10
LOG_LV_INFO = 20
LOG_LV_WARNING = 30
LOG_LV_ERROR = 40
LOG_LV_CRITICAL = 50

DEFAULT_LOG_PATH = "/opt/Future/system/log"
LOG_SIZE = 1024*1024 # 1MB
LOG_BACKUP_CNT = 4
LOG_NAME = "web_server"