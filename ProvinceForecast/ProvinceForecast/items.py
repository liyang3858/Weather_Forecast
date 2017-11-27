# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ProvinceforecastItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    ProvinceCode = scrapy.Field()
    ProvinceName = scrapy.Field()
    PublishDate = scrapy.Field()
    WarningInfo = scrapy.Field()
    OtherDescription = scrapy.Field()
    TrendImage = scrapy.Field()
    ForecastDescription = scrapy.Field()
    HealthTips = scrapy.Field()
    SceneryImagesPath = scrapy.Field()
    created = scrapy.Field()
    date_time = scrapy.Field()
