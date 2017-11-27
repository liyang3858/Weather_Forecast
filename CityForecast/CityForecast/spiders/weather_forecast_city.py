# -*- coding:utf8 -*-
# Author: Liyang <13643545721@163.com>
# Create_date: 2017-11-22
# 爬取内容：全国空气质量预报信息发布系统（http://106.37.208.228:8082/）- 城市预报

import scrapy
from scrapy.selector import Selector
from CityForecast.items import CityforecastItem 
from CityForecast.helper import *
import sys
import re
import platform

reload(sys)
sys.setdefaultencoding('utf-8')

class Weather_forecast_city_spider(scrapy.Spider):
    name = "WeatherForecastCitySpider"

    def start_requests(self):
        city_url = 'http://106.37.208.228:8082/CityForecast'
        yield scrapy.Request(city_url, callback = self.parse_get_city, headers = {'Referer':'http://106.37.208.228:8082/'})
    
    
    def parse_get_city(self, response):
        citylist = response.xpath('//*[@id="sel_city"]//a[@data-id]')
        for i in xrange(0,len(citylist)):
            city_code = get_element_of_list(citylist[i].xpath('./@data-id').extract())
            city_name = get_element_of_list(citylist[i].xpath('./text()').extract())
            
            url = 'http://106.37.208.228:8082/CityForecast'
            yield scrapy.FormRequest(url, callback = self.parse_data, formdata = {'CityCode':city_code}, headers = {'Referer':'http://106.37.208.228:8082/'}, meta = {'city_code':city_code, 'city_name':city_name})
    
    
    def parse_data(self, response):
        city_code = response.meta['city_code']
        city_name = response.meta['city_name']
        
        #网页获取的张家口市行政编码有误（网页为131200，实际为130700），因此行政编码统一从表polls_city获得。经度、纬度从表polls_city获得。
        (Latitude, Longitude, CityCode) = city2code(city_name)
        hourAqiDiv = response.xpath('//*[@id="yubaoTab"]//div[@class="hourAqiDiv"]') 
        date_time = get_element_of_list(hourAqiDiv[0].xpath('.//div[@class="aqi_title"]/p/text()').extract())
        created = int(str2time(get_now())[0:10])
        
        PotentialInfo_label = response.xpath('//*[@id="spreadInfo"]')
        if len(PotentialInfo_label) != 0:
            PotentialInfo = get_element_of_list(PotentialInfo_label.xpath('./text()').extract()).strip()
            PotentialInfo = re.sub('\n', '', PotentialInfo)
        else:
            PotentialInfo = ''

        #24小时预报信息
        Air24Index_From = int(get_element_of_list(hourAqiDiv[0].xpath('.//p[@class="aqi_value_number"]/span[1]/text()').extract()))
        Air24Index_To = int(get_element_of_list(hourAqiDiv[0].xpath('.//p[@class="aqi_value_number"]/span[2]/text()').extract()))
        Primary24Pollutant_list = hourAqiDiv[0].xpath('.//p[@class="first_pollutant"]//text()').extract()
        Primary24Pollutant = ''.join(Primary24Pollutant_list)
        Primary24Pollutant = re.sub(u'首要污染物:', '', Primary24Pollutant)
        
        #48小时预报信息
        Air48Index_From = int(get_element_of_list(hourAqiDiv[1].xpath('.//p[@class="aqi_value_number"]/span[1]/text()').extract()))
        Air48Index_To = int(get_element_of_list(hourAqiDiv[1].xpath('.//p[@class="aqi_value_number"]/span[2]/text()').extract()))
        Primary48Pollutant_list = hourAqiDiv[1].xpath('.//p[@class="first_pollutant"]//text()').extract()
        Primary48Pollutant = ''.join(Primary48Pollutant_list)
        Primary48Pollutant = re.sub(u'首要污染物:', '', Primary48Pollutant)

        #72小时预报信息
        Air72Index_From = int(get_element_of_list(hourAqiDiv[2].xpath('.//p[@class="aqi_value_number"]/span[1]/text()').extract()))
        Air72Index_To = int(get_element_of_list(hourAqiDiv[2].xpath('.//p[@class="aqi_value_number"]/span[2]/text()').extract()))
        Primary72Pollutant_list = hourAqiDiv[2].xpath('.//p[@class="first_pollutant"]//text()').extract()
        Primary72Pollutant = ''.join(Primary72Pollutant_list)
        Primary72Pollutant = re.sub(u'首要污染物:', '', Primary72Pollutant)
        
        """print '-'*20
        print u'编码对比',city_code,CityCode
        print city_name  
        print Latitude,Longitude
        print created
        print date_time
        print PotentialInfo
        print Air24Index_From
        print Air24Index_To
        print Primary24Pollutant
        print Air48Index_From
        print Air48Index_To
        print Primary48Pollutant
        print Air72Index_From
        print Air72Index_To
        print Primary72Pollutant
        """

        item = CityforecastItem()

        item['CityCode'] = str(CityCode)
        item['Name'] = city_name.encode('utf8')
        item['Air24Index_From'] = Air24Index_From
        item['Air24Index_To'] = Air24Index_To
        item['Primary24Pollutant'] = Primary24Pollutant.encode('utf8')
        item['Air48Index_From'] = Air48Index_From
        item['Air48Index_To'] = Air48Index_To
        item['Primary48Pollutant'] = Primary48Pollutant.encode('utf8')
        item['Air72Index_From'] = Air72Index_From
        item['Air72Index_To'] = Air72Index_To
        item['Primary72Pollutant'] = Primary72Pollutant.encode('utf8')
        item['PotentialInfo'] = PotentialInfo.encode('utf8')
        item['Latitude'] = Latitude
        item['Longitude'] = Longitude
        item['created'] = created
        item['date_time'] = date_time.encode('utf8')

        yield item
        

#输入城市名称，返回经度、纬度、城市行政编码 
def city2code(city_name):
    import traceback
    import sqlite3
    import os

    try:
        city_name = city_name.decode("utf8")
    except UnicodeDecodeError:
        pass
    
    db_path = os.path.dirname(os.path.abspath(__file__)) + '/../city.db'
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    sql = '''select `x`,`y`,`code` from polls_city 
             where `name`=?
          '''
    rows = cursor.execute(sql, (city_name,))
    rows = cursor.fetchall()

    rows_len = len(rows)

    #什么也没找到，则报错
    if rows_len == 0:
        raise Exception("Cann't find %s in mysql!" % city_name)
    else:
        return rows[0][0],rows[0][1],rows[0][2]
    
    conn.close()
