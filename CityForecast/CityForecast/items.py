# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class CityforecastItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    CityCode = scrapy.Field()
    Name = scrapy.Field()
    Air24Index_From = scrapy.Field()
    Air24Index_To = scrapy.Field()
    Primary24Pollutant = scrapy.Field()
    Air48Index_From = scrapy.Field()
    Air48Index_To = scrapy.Field()
    Primary48Pollutant = scrapy.Field()
    Air72Index_From = scrapy.Field()
    Air72Index_To = scrapy.Field()
    Primary72Pollutant = scrapy.Field()
    PotentialInfo = scrapy.Field()
    Latitude = scrapy.Field()
    Longitude = scrapy.Field()
    created = scrapy.Field()
    date_time = scrapy.Field()
