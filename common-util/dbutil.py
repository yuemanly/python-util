# _*_ coding:utf-8 _*_

from logutil import Logger
from configutil import ConfigUtil
import sys
import pymysql
import time
from sshtunnel import SSHTunnelForwarder
from DBUtils.PooledDB import PooledDB

class DBUtil(object):

    # 传入需要连接的数据库的名称dbname和待执行的sql语句sql
    def __init__(self,configUtil,host,port,username,password,db):
        self.config = configUtil
        self.host = host
        self.port = port
        self.db = db
        self.username = username
        self.password = password
        self.logger = Logger("db",configUtil).getlog()

        self.pool = PooledDB(creator=pymysql,
                             mincached=1,
                             maxcached=20,
                             host=self.host,
                             port=int(self.port),
                             user=self.username,
                             passwd=self.password,
                             db=self.db,
                             use_unicode=True,
                             charset="utf8")

    def get_connection(self):
        try:
            mysql_con = self.pool.connection()
            return mysql_con
        except Exception as e:
            self.logger.error(e)
            for i in range(3):
                try:
                    time.sleep(5)
                    mysql_con = self.pool.connection()
                    return mysql_con
                except Exception as e:
                    self.logger.error(e)
                    self.logger.error("数据库连接异常执行" + str(i + 1) + "次连接")
            sys.exit(1)

    def release_connection(self, connection):
        try:
            connection.close()
        except Exception as e:
            self.logger.error(e)
            self.logger.error("mysql connection 关闭异常")
            sys.exit(1)


    def query(self,sql):

        # def query(self, sql):
        #     results = ''
        #     conn = pymysql.connect(host=self.host,
        #                            port=self.port,
        #                            user=self.username,
        #                            passwd=self.password,
        #                            db=self.db)
        #     cursor = conn.cursor()
        #     try:
        #         # 执行SQL语句
        #         cursor.execute(sql)
        #         # 获取所有记录列表
        #         results = cursor.fetchall()
        #     except Exception as data:
        #         print('Error: 执行查询失败，%s' % data)
        #
        #     conn.close()
        #     return results

        try:
            connection = self.get_connection()
            cursor = connection.cursor()
            cursor.execute(sql)
            rows = cursor.fetchall()
            cursor.close()
            self.release_connection(connection)
            return rows
        except Exception as e:
            self.logger.error("执行查询:%s 出错" %(e))
            sys.exit(1)

    def insert_dict_into_table(self,table_name,data_dict):
        cols = ','.join(data_dict.keys())
        qmarks = ','.join(['%s'] * len(data_dict))
        insert_sql = 'insert into %s (%s) values(%s)' % (table_name,cols,qmarks)
        self.insert(insert_sql,data_dict.values())

    def insert(self,sql,values):
        try:
            connection = self.get_connection()
            cursor = connection.cursor()
            cursor.execute(sql,values)
            connection.commit()
            cursor.close()
            self.release_connection(connection)
        except Exception as e:
            self.logger.error("执行查询:%s 出错:%s" %(sql,e))
            connection.rollback()
            sys.exit(1)
        finally:
            self.release_connection(connection)

    def delete(self,sql):
        try:
            connection = self.get_connection()
            cursor = connection.cursor()
            cursor.execute(sql)
            connection.commit()
            cursor.close()
            self.release_connection(connection)
        except Exception as e:
            self.logger.error("执行查询:%s 出错:%s" %(sql,e))
            connection.rollback()
            sys.exit(1)
        finally:
            self.release_connection(connection)


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