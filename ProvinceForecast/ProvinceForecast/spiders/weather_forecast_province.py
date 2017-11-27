# -*- coding:utf8 -*-
# Author: Liyang <13643545721@163.com>
# Create_date: 2017-11-22
# 爬取内容：全国空气质量预报信息发布系统（http://106.37.208.228:8082/）- 省域预报

import scrapy
from scrapy.selector import Selector
from ProvinceForecast.items import ProvinceforecastItem 
from ProvinceForecast.helper import *
import sys
import re
import platform
import json

reload(sys)
sys.setdefaultencoding('utf-8')

class Weather_forecast_province_spider(scrapy.Spider):
    name = "WeatherForecastProvinceSpider"
    
    def start_requests(self):
        province_url = 'http://106.37.208.228:8082/ProvinceForecast/GetGlobalInfo'
        yield scrapy.Request(province_url, callback = self.parse_data, headers = {'Referer':'http://106.37.208.228:8082/'})
         
    
    def parse_data(self, response):
        data_list = json.loads(response.body)
        for prov_dic in data_list:
            ProvinceCode = prov_dic['ProvinceCode'] 
            ProvinceName = prov_dic['ProvinceName']
            PublishDate = prov_dic['PublishDate']
            WarningInfo = prov_dic['WarningInfo']
            OtherDescription = prov_dic['OtherDescription']
            TrendImage = prov_dic['TrendImage'] if prov_dic['TrendImage'] != None else ''  #趋势图没有完整路径，只有图片名称。
            ForecastDescription = prov_dic['ForecastDescription']
            ForecastDescription = re.sub('\n', '', ForecastDescription) #去掉换行符
            ForecastDescription = re.sub(' ', '', ForecastDescription) #去掉空格
            HealthTips = prov_dic['HealthTips']
            SceneryImagesPath = 'http://106.37.208.228:8082' + prov_dic['SceneryImagesPath']  #风景图完整访问地址
            created = int(str2time(get_now()))
            date_time = get_now()[0:10]

            """print '-'*20
            print ProvinceCode  
            print ProvinceName
            print PublishDate
            print WarningInfo
            print 'o',OtherDescription
            print 't',TrendImage
            print 'f',ForecastDescription
            print HealthTips
            print SceneryImagesPath
            print created
            print date_time

            """
            item = ProvinceforecastItem()

            item['ProvinceCode'] = ProvinceCode.encode('utf8')
            item['ProvinceName'] = ProvinceName.encode('utf8')
            item['PublishDate'] = PublishDate.encode('utf8')
            item['WarningInfo'] = WarningInfo.encode('utf8')
            item['OtherDescription'] = OtherDescription.encode('utf8')
            item['TrendImage'] = TrendImage.encode('utf8')
            item['ForecastDescription'] = ForecastDescription.encode('utf8')
            item['HealthTips'] = HealthTips.encode('utf8') 
            item['SceneryImagesPath'] = SceneryImagesPath.encode('utf8')
            item['created'] = created
            item['date_time'] = date_time.encode('utf8')

            yield item
