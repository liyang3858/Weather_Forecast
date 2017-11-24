# -*- coding:utf8 -*-
# Author: Liyang <13643545721@163.com>
# Create_date: 2017-11-22
# 爬取内容：全国空气质量预报信息发布系统（http://106.37.208.228:8082/）- 区域预报

import scrapy
from scrapy.selector import Selector
from AreaForecast.items import AreaforecastItem  
from AreaForecast.helper import *
import sys
import re
import platform
#import math
#import datetime
#from datetime import timedelta
import time
import json

reload(sys)
sys.setdefaultencoding('utf-8')

class Weather_forecast_area_spider(scrapy.Spider):
    name = "WeatherForecastAreaSpider"
    start_urls = ('http://106.37.208.228:8082/AreaForecast',)

    def parse(self, response):
        arealist = response.xpath('//*[@id="areaList"]//a[@areacode]')
        for i in xrange(0,len(arealist)):
            area_code = get_element_of_list(arealist[i].xpath('./@areacode').extract())
            area_name = get_element_of_list(arealist[i].xpath('./text()').extract())
            
            area_url = 'http://106.37.208.228:8082/AreaForecast/ChangeArea?areaCode=' + area_code + '&strForecastType=1'
            yield scrapy.Request(area_url, callback = self.parse_data, headers = {'Referer':'http://106.37.208.228:8082/'}, meta = {'area_code':area_code, 'area_name':area_name})
    
    
    def parse_data(self, response):
        area_code = response.meta['area_code']
        area_name = response.meta['area_name']
        
        data_dic = json.loads(response.body)
        forecast_description = data_dic['ForecastDescription'].strip()
        forecast_description = re.sub('\n', '', forecast_description)
        created = int(str2time(get_now()))
        date_time = get_now()[0:10]
        
        """print '-'*20
        print area_code
        print area_name  
        print forecast_description
        print created
        print date_time
        """

        item = AreaforecastItem()

        item['area_code'] = area_code.encode('utf8')
        item['area_name'] = area_name.encode('utf8')
        item['forecast_description'] = forecast_description.encode('utf8')
        item['created'] = created 
        item['date_time'] = date_time.encode('utf8')
        
        yield item
