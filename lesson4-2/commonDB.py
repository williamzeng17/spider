# coding: utf-8

import mysql.connector
import re
import time
import sys

reload(sys)
sys.setdefaultencoding('utf8')


class CommonDB:
    def __init__(self, config):

        try:
            self.conn = mysql.connector.connect(
                user=config['user'],
                password=config['password'],
                host=config['host'],
                port=config['port'],
                database=config['database'],
                use_unicode=config['unicode']
            )
            self.cursor = self.conn.cursor(buffered=True, dictionary=True)
        except mysql.connector.Error as e:
            print('connect database error!{}'.format(e))

        self.keys = []  # 数据库的字段
        self.sql = ''  # 要执行的sql语句
        self.table = ''
        self.primaryKey = ''

    def __del__(self):
        self.cursor.close()
        self.conn.close()

    def checkParams(self, params):
        filterParams = {}
        for key in params:
            if key in self.keys:
                filterParams[key] = params[key]
        return filterParams

    def checkFields(self, fields):
        keyStr = ''
        if None is fields or '' == fields:
            fields = self.keys

        for key in fields:
            if key in self.keys:
                keyStr = '%s , `%s`' % (keyStr, key)
        return keyStr.strip(', ')

    def checkWhere(self, where):
        condition = ''
        where = self.checkParams(where)
        for key in where:
            val = str(where[key]).strip()
            if re.match(r'(=|>|<|>=|<=|!=)', val) or val == 'is null':
                condition = '%s AND (`%s` %s)' % (condition, key, where[key])
            else:
                condition = "%s AND (`%s`='%s')" % (condition, key, where[key])
        return condition.strip(' AND')

    def sqlExec(self, data=None):
        if None != self.sql:
            try:
                if None is not data:
                    self.cursor.execute(self.sql, data)
                else:
                    self.cursor.execute(self.sql)
            except mysql.connector.Error as e:
                print('sql process error!||errmsg:%s||sql:%s' % (format(e), self.sql))

    def insertOne(self, params):
        """
        插入一条数据
        :param params:
        :return:
        """
        params = self.checkParams(params)
        params['_create_time'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        params['_modify_time'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))

        fields = ''
        valueStr = ''
        values = []
        for key in params:
            val = str(params[key]).encode('utf-8', errors='ignore')
            fields += '`%s`,' % key
            valueStr += '%s, '
            values.append(val)
        fields = fields.strip(', ')
        valueStr = valueStr.strip(', ')
        self.sql = 'INSERT %s(%s) VALUES (%s)' % (self.table, fields, valueStr)
        self.sqlExec(values)
        self.conn.commit()

    def getOne(self, where, fields=''):
        """
        获取一条数据
        :param fields:
        :param where:
        :return:
        """
        fields = self.checkFields(fields)
        condition = self.checkWhere(where)
        self.sql = 'SELECT %s FROM %s WHERE %s order by %s limit 1'
        params = [fields, self.table, condition, self.primaryKey]
        self.sqlExec(params)
        return self.cursor.fetchone()

    def getMulti(self, where=None, page=0, offset=0, fields=None):
        """
        获取多条数据
        :param where:
        :param page:
        :param offset:
        :param fields:
        :return:
        """
        fields = self.checkFields(fields)
        condition = self.checkWhere(where)
        if page == 0:
            limit = '%d' % offset
        else:
            limit = '%d, %d' % ((page - 1) * offset, offset)
        self.sql = 'SELECT %s FROM %s WHERE %s order by %s limit %s'
        params = [fields, self.table, condition, self.primaryKey, limit]
        self.sqlExec(params)
        return self.cursor.fetchall()

    def updateOne(self, primaryVal='', params=None, where=None):
        """
        更新一条数据
        :param params:
        :param where:
        :return:
        """
        params = self.checkParams(params)
        if None is where:
            where = {}
        params['_modify_time'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        setParam = ''
        values = []
        for key in params:
            val = str(params[key]).encode('utf-8', errors='ignore')
            setParam += '`%s` = %s, ' % (key, '%s')
            values.append(val)
        setParam = setParam.strip(', ')
        if primaryVal is not (None or ''):
            where['id'] = primaryVal
        condition = self.checkWhere(where)
        self.sql = 'UPDATE %s SET %s WHERE %s' % (self.table, setParam, condition)
        self.sqlExec(values)
        self.conn.commit()
