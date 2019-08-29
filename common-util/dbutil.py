# _*_ coding:utf-8 _*_

from logutil import Logger
from configutil import ConfigUtil
import pymysql
from sshtunnel import SSHTunnelForwarder
from DBUtils.PooledDB import PooledDB

class DBUtil(object):

    # 传入需要连接的数据库的名称dbname和待执行的sql语句sql
    def __init__(self,configUtil,host,port,username,password,db):
        self.configUtil = configUtil
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.db = db

    def query_ssh(self,sql,ssh_config):
        results = ''
        with SSHTunnelForwarder(
                (ssh_config['host'],ssh_config['port']),
                ssh_username=ssh_config['username'],
                ssh_password=ssh_config['password'],
                remote_bind_address=(self.host, self.port)) as server:
            conn = pymysql.connect(host='127.0.0.1',  # 此处必须是是127.0.0.1
                                   port=server.local_bind_port,
                                   user=self.username,
                                   passwd=self.password,
                                   db=self.db)
            cursor = conn.cursor()
            try:
                # 执行SQL语句
                cursor.execute(sql)
                # 获取所有记录列表
                results = cursor.fetchall()
            except Exception as data:
                print('Error: 执行查询失败，%s' % data)

            conn.close()
            return results

    def query(self,sql):
        results = ''
        conn = pymysql.connect(host=self.host,
                               port=self.port,
                               user=self.username,
                               passwd=self.password,
                               db=self.db)
        cursor = conn.cursor()
        try:
            # 执行SQL语句
            cursor.execute(sql)
            # 获取所有记录列表
            results = cursor.fetchall()
        except Exception as data:
            print('Error: 执行查询失败，%s' % data)

        conn.close()
        return results


if __name__ == '__main__':
    pass