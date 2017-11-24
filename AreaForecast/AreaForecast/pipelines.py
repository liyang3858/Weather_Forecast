# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import MySQLdb

class AreaforecastPipeline(object):
    
    def __init__(self):
        self.MYSQL_HOST = 'rdsvy5g7kci8vffh3fdlo.mysql.rds.aliyuncs.com'
        self.MYSQL_DBNAME = 'monitordata'
        self.MYSQL_USER = 'tsinghua'
        self.MYSQL_PASSWD = '6haSWUju'
        self.port = 3888
        self.conn=MySQLdb.connect(host=self.MYSQL_HOST,user=self.MYSQL_USER,passwd=self.MYSQL_PASSWD,db=self.MYSQL_DBNAME,charset="utf8",port=self.port)
      
    def process_item(self, item, spider):
        self.cursor = self.conn.cursor(MySQLdb.cursors.DictCursor)
        # SQL 插入语句
        
        area_code = item['area_code']
        area_name = item['area_name']
        forecast_description = item['forecast_description']
        created = item['created']
        date_time = item['date_time']
      
        sql = """INSERT  INTO air_area_predict(`area_code`,`area_name`,`forecast_description`,`created`,`date_time`) VALUES (%s,%s,%s,%s,%s)"""
        sql2 = """select * from air_area_predict where `area_code`=%s and `area_name`=%s and `date_time`=%s """
        try:
            self.cursor.execute(sql2,[area_code,area_name,date_time])
            if self.cursor.fetchall():
                pass
            else:
                self.cursor.execute(sql,[area_code,area_name,forecast_description,created,date_time])
                self.conn.commit()
        except KeyError, e: 
            print e
            pass
        return item

    def close_spider(self,spider):
        self.cursor.close()
        self.conn.close()
