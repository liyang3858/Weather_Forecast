# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


import MySQLdb

class CityforecastPipeline(object):
    
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
        
        CityCode = item['CityCode']
        Name = item['Name']
        Air24Index_From = item['Air24Index_From']
        Air24Index_To = item['Air24Index_To']
        Primary24Pollutant = item['Primary24Pollutant']
        Air48Index_From = item['Air48Index_From']
        Air48Index_To = item['Air48Index_To']
        Primary48Pollutant = item['Primary48Pollutant']
        Air72Index_From = item['Air72Index_From']
        Air72Index_To = item['Air72Index_To']
        Primary72Pollutant = item['Primary72Pollutant']
        PotentialInfo = item['PotentialInfo']
        Latitude = item['Latitude']
        Longitude = item['Longitude']
        created = item['created']
        date_time = item['date_time']
      
        sql = """INSERT  INTO air_predict(`CityCode`,`Name`,`Air24Index_From`,`Air24Index_To`,`Primary24Pollutant`,`Air48Index_From`,`Air48Index_To`,`Primary48Pollutant`,`Air72Index_From`,`Air72Index_To`,`Primary72Pollutant`,`PotentialInfo`,`Latitude`,`Longitude`,`created`,`date_time`) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
        sql2 = """select * from air_predict where `CityCode`=%s and `Name`=%s and `date_time`=%s """
        try:
            self.cursor.execute(sql2,[CityCode,Name,date_time])
            if self.cursor.fetchall():
                pass
            else:
                self.cursor.execute(sql,[CityCode,Name,Air24Index_From,Air24Index_To,Primary24Pollutant,Air48Index_From,Air48Index_To,Primary48Pollutant,Air72Index_From,Air72Index_To,Primary72Pollutant,PotentialInfo,Latitude,Longitude,created,date_time])
                self.conn.commit()
        except KeyError, e: 
            print e
            pass
        return item

    def close_spider(self,spider):
        self.cursor.close()
        self.conn.close()
