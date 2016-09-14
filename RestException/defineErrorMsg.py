#!/usr/bin/env python
#coding=utf8

__author__ = 'mjhans'

"""
	작성자: 문중현
	내용 :
		Restful API 예외처리 코드 및 메시지 정의

"""

# ERROR CODE
# tornado Server ERROR 0x01

T_SVRERR = 0x01
T_UNKNOWN = 0x9999 | T_SVRERR
T_START_ERROR = 0x0001 | T_SVRERR




# ERROR msg
REST_ERROR_MSG = {
	T_START_ERROR : "Tornado server start error"
}