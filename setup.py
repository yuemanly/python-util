# -*- coding:utf-8 -*-
#模块的安装配置文件

#from distutils.core import setup
from setuptools import setup,find_packages


setup(
    name="common-util",
    version="1.0",
    packages=find_packages(),
    author='yuemanly',
    zip_safe = False
)

