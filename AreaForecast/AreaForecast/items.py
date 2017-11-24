# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class AreaforecastItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    area_code = scrapy.Field()
    area_name = scrapy.Field()
    forecast_description = scrapy.Field()
    created = scrapy.Field()
    date_time = scrapy.Field()
