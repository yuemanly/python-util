# -*- coding:utf-8 -*-
#通用的工具类

class CommonUtil(object):

    @staticmethod
    def convert_byte_mb(self,bytes,ndigits=2):
        return round(bytes*1.0 /1024 /1024 ,ndigits)

    @staticmethod
    def convert_byte_gb(self,bytes,ndigits=2):
        return round(bytes*1.0 /1024 /1024 /1024,ndigits)

    @staticmethod
    def convert_byte_tb(self,bytes,ndigits=2):
        return round(bytes*1.0 /1024 /1024 /1024 /1024,ndigits)
