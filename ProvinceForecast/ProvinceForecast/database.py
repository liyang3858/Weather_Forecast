#!/usr/bin/python2.7
#coding: utf-8
import sys
import os.path
import ConfigParser
import MySQLdb
import MySQLdb.cursors
import traceback
from random import random
from time import sleep
from aliyun.ots2 import *
import helper

reload(sys)
sys.setdefaultencoding('utf-8')

class DatabaseClient(object):
    def get_conf(self,db_name):
        path = os.path.dirname(__file__)

        if helper.get_pc_name() in helper.ali_server or helper.get_pc_name() in helper.test_server:
            name = 'database.cfg'
        else:
            name = 'database_test.cfg'

        name = os.path.join(path, name)

        config = ConfigParser.ConfigParser()
        config.read(name)

        return dict([(option, config.get( db_name, option)) for option in config.options(db_name)])

class MysqlClient(DatabaseClient):
    mysql_connection_num = 0

    def __init__(self):
        self.conn = None

    def connect(self, db):
        self.conn = None

        while self.get_mysql_connection_num() >= 50:#MAX_CONNECTION_NUM:
            sleep(random())

        conf = self.get_conf(db)

        host = conf['host']
        user = conf['user']
        password = conf['password']
        database = conf['database']
        charset = conf['charset']
        port = conf['port']

        port = int(port) if port else 3306

        try:
            MySQLdb = __import__('MySQLdb')
            conn = MySQLdb.connect(host=host, user=user, passwd=password, db=database, port=port, cursorclass=MySQLdb.cursors.DictCursor)
            self.conn = conn
            self.add_mysql_connection_num()
            self.execute('set names ' + charset)
        except Exception,e:
            print e
            return None

    def close(self):
        if self.conn != None:
            self.conn.close()
            self.minus_mysql_connection_num()

    def execute(self, sql, data=None):
        cur = self.conn.cursor()
        try:
            cur.execute(sql, data)
        except MySQLdb.OperationalError, e:
            if 'No database selected' in str(e):
                pass
        finally:
            cur.close()
        self.conn.commit()

    def executemany(self, sql, data):
        cur = self.conn.cursor()
        cur.executemany(sql, data)
        cur.close()
        self.conn.commit()

    def query(self, sql, data=None):
        cur = self.conn.cursor()
        try:
            if data:
                cur.execute(sql, data)
            else:
                cur.execute(sql)
        except MySQLdb.Error,e:
            print "Mysql Error %d: %s" % (e.args[0], e.args[1])
            print sql
            print data;
            print e
            print "-----------"

        rows = cur.fetchall()
        cur.close()
        return rows
    
    @classmethod
    def add_mysql_connection_num(cls):
        cls.mysql_connection_num += 1

    @classmethod
    def minus_mysql_connection_num(cls):
        if cls.mysql_connection_num > 0:
            cls.mysql_connection_num -= 1
    
    def get_mysql_connection_num(self):
        return self.mysql_connection_num

class otsClient(DatabaseClient):
    def get_OTS(self, db_name="ots"):
        db_name = "ots" if helper.get_pc_name() in helper.ali_server else "ots_test"
        conf = self.get_conf(db_name)

        end_point = conf['end_point']
        access_id = conf['access_key_id']
        access_key = conf['access_key_secret']
        instance_name = conf['instance_name']

        return OTSClient(end_point, access_id, access_key, instance_name)

    def put_row(self, item, db_name="ots"):
        ots_client = self.get_OTS(db_name)
        consumed = ots_client.put_row(item.talbe, item.condition, item.primary_key, item.attribute_cols)

        return consumed

    def batch_put_row(self, batch_list, db_name="ots"):
        ots_client = self.get_OTS(db_name)
        #code below is from the example given by ots

        try:
            batch_write_response = ots_client.batch_write_row(batch_list)
        except OTSServiceError, e:
            print "Notice!!!! " + str(e)
            batch_write_response = []
        except Exception, e:
            traceback.print_exc();
            print "exception caught when writing: " + str(e)
            print "bad data:"
            for bad_data in batch_list:
                for each_bad_data in bad_data['put']:
                    print each_bad_data.primary_key;print each_bad_data.attribute_columns; print "--------------"
            return
        def add_batch_write_item(batch_list, table_name, operation, item):
            for table_item in batch_list:
                if table_item.get('table_name') == table_name:
                    operation_item = table_item.get(operation)
                    if not operation_item:
                        table_item[operation] = [item]
                    else:
                        operation_item.append(item)
                    return
            # not found
            table_item = {'table_name':table_name, operation:[item]}
            batch_list.append(table_item)

        retry_count = 0
        operation_list = ['put', 'update', 'delete']
        while retry_count < 3:
            print("---------------no.%s retry------------" % str(retry_count+1))
            failed_batch_list = []
            for i in range(len(batch_write_response)):
                table_item = batch_write_response[i]
                for operation in operation_list:
                    operation_item = table_item.get(operation)
                    if not operation_item:
                        continue
                    print u'操作：%s' % operation
                    for j in range(len(operation_item)):
                        row_item = operation_item[j]
                        print u'操作是否成功：%s' % row_item.is_ok
                        if not row_item.is_ok:
                            print u'错误码：%s' % row_item.error_code
                            print u'错误信息：%s' % row_item.error_message
                            add_batch_write_item(failed_batch_list, batch_list[i]['table_name'], operation, batch_list[i][operation][j])
                        else:
                            print u'本次操作消耗的写CapacityUnit为：%s' % row_item.consumed.write

            if not failed_batch_list:
                break
            retry_count += 1
            batch_list = failed_batch_list
            batch_write_response = ots_client.batch_write_row(batch_list)

    def create_table(self):
        ots_client = self.get_OTS("ots")
        schema_of_primary_key = [("id", "INTEGER"),]
        table_meta = TableMeta("webbot_page", schema_of_primary_key)
        reserved_throughput = ReservedThroughput(CapacityUnit(0, 0))
        ots_client.create_table(table_meta, reserved_throughput)
        print(u"表已创建")

if __name__ == '__main__':
    #otsClient().create_table()
    print ali_server
    pass


'''
    primary_key = {"id": 0,}
    attribute_columns = {"title": "Webbot Diagnostic Page0", "text": "imissu0",}
    condition = Condition('EXPECT_NOT_EXIST')
    put_row_item0 = PutRowItem(condition, primary_key, attribute_columns)

    primary_key = {"id": 1,}
    attribute_columns = {"title": "Webbot Diagnostic Page1", "text": "imissu1",}
    condition = Condition('EXPECT_NOT_EXIST')
    put_row_item1 = PutRowItem(condition, primary_key, attribute_columns)

    primary_key = {"id": 2,}
    attribute_columns = {"title": "Webbot Diagnostic Page2", "text": "imissu2",}
    condition = Condition('EXPECT_NOT_EXIST')
    put_row_item2 = PutRowItem(condition, primary_key, attribute_columns)

    table_item = {"table_name": "webbot_page", "put": [put_row_item0, put_row_item2, put_row_item1,], }
    batch_list = [table_item, ]

    otsClient().batch_put_row(batch_list)
'''
