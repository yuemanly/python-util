# -*- coding:utf-8 -*-

import logging
import logging.handlers
import logging.config
import os

class Logger(object):
    def __init__(self, name,configUtil,logFile=None,logDir=None):
        self.config = configUtil
        # 创建一个logger
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.INFO)

        formatter = logging.Formatter('%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s')

        # 用于写入日志文件
        if logDir == None:
            log_dir = self.config.get("log.dir")
            print(log_dir)
        else:
            log_dir = logDir
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)

        if logFile == None:
            log_file = log_dir + "/" + name + ".log"
        else:
            log_file = log_dir + "/" + logFile
        handler = logging.handlers.TimedRotatingFileHandler(log_file, when="midnight", backupCount=10)
        # 输出到控制台
        # handler = logging.StreamHandler()
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)

    def getlog(self):
        return self.logger

if __name__ == '__main__':
    config = {'host': '74.82.212.212','port': 26439 ,'user': 'root','password': 'HHbQo9ki8jTb',"log.dir":"/Users/liusheng/Downloads/"}
    a = Logger('a',config)
    a.getlog()