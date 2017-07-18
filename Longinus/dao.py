# -*- coding: UTF-8 -*-

import pymysql
from django.db import connection


class Dao(object):
    del __init__(self, MysqlHost, MysqlPort, MysqlUser, MysqlPasswd):
        self.host = MysqlHost
        self.port = MysqlPort
        self.user = MysqlUser
        self.passwd = MysqlPasswd

    def mysqlFetchOne(self, sql, database):
        result = None
        conn = None
        cur = None

        try:
            conn = pymysql.connect(host = self.host,
                                   port = self.port,
                                   user = self.user,
                                   passwd = self.passwd,
                                   db = database,
                                   charset = 'utf8mb4')
            cur = conn.cursor()
            cur.execute(sql)
            result = cur.fetchone()

        except pymysql.Error as e:
            print("MySql Error %d: %s" % (e.args[0], e.args[1]))

        finally:
            if cur is not None:
                cur.close()
            if conn is not None:
                conn.close()

        return result


    def mysqlFetchAll(self, sql, database):
        result = None
        conn = None
        cur = None

        try:
            conn = pymysql.connect(host = self.host,
                                   port = self.port,
                                   user = self.user,
                                   passwd = self.passwd,
                                   db = database,
                                   charset = 'utf8mb4')
            cur = conn.cursor()
            cur.execute(sql)
            result = cur.fetchall()

        except pymysql.Error as e:
            print("MySql Error %d: %s" % (e.args[0], e.args[1]))

        finally:
            if cur is not None:
                cur.close()
            if conn is not None:
                conn.close()

        return result


    def createDatabase(self, dbName):
        result = None
        conn = None
        cur = None

        sql = "create database %s;" % (dbName)

        try:
            conn = pymysql.connect(host=masterHost,
                                   port=masterPort,
                                   user=masterUser,
                                   passwd=masterPassword,
                                   charset='utf8mb4')
            cur = conn.cursor()
            cur.execute(sql)
            result = 'complete'

        except pymysql.Error as e:
            print("MySql Error %d: %s" % (e.args[0], e.args[1]))

        finally:
            if cur is not None:
                cur.close()
            if conn is not None:
                conn.close()

        return result
