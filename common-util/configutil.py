# -*- coding:utf-8 -*-

import os
# import sys

'''
读取配置文件
'''


class ConfigUtil(object):
    def __init__(self,project_path=None,project_env=None):
        # envpath = os.getenv("ETL_SCHEDULE_PATH", "")
        # if envpath == "" or len(envpath) == 0:  # test/config.ini 可以随意设置
        #     path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        #     config_path = path + "/config/test/config.ini"
        # else:
        #     config_path = envpath + "/config/product/config.ini"
        # self.config = self.load_config(config_path)

        #加载项目自身的配置信息
        if project_env == None:
            project_env = os.getenv("PYTHON_PROJECT_ENV", "test")
        if project_path != None:
           config_file_path =  project_path + os.path.sep + "config/" + project_env + os.path.sep + "config.ini"
           print(config_file_path)
           self.config = self.load_config(config_file_path)

        #加载全局公共的配置信息
        # if self.config.has_key("common_config_project_path"):
        #     common_config_project_path = self.config.get("common_config_project_path")
        #     common_config_file_path = common_config_project_path + os.path.sep + project_env + os.path.sep + "common-config.ini"
        #     self.config.update(self.load_config(common_config_file_path))




    def load_config(self, path):
        config = {}
        config_file_handler = open(path)
        if config_file_handler is None:
            raise IOError("无法读取配置文件")
        for line in config_file_handler.readlines():
            if line and len(line.strip()) > 0 and (not line.startswith("#")):
                key_value = line.strip().split("=", 1)
                if len(key_value) == 2:
                    key = key_value[0].strip()
                    value = key_value[1].strip()
                    config[key] = value
                else:
                    print("无法读取配置项:" + str(line))
        return config

    def get(self, name):
        value = self.config.get(name)
        if not value:
            raise Exception("读取配置" + name + "失败")
        return value

    def getOrElse(self, name, default=None):
        value = self.config.get(name)
        if value is None or len(value.strip()) == 0:
            return default
        else:
            return value

    def getBooleanOrElse(self, name, default):
        value = self.config.get(name)
        if value is None or len(value.strip()) == 0:
            return default
        else:
            value = value.upper()
            if value == "TRUE":
                return True
            else:
                return False

# a = ConfigUtil('/Users/liusheng/Downloads/github/tools/wuhao/wh_tools_master')
# a.get('mysql.bi_result.t9.hos')
# print(a.config.get('mysql.bi_result.t9.host'))
