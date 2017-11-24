# -*- coding: utf-8 -*-

# Scrapy settings for CompanyPollution_lca project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#
import helper

BOT_NAME = '神马'
LOG_LEVEL = 'WARNING'
LOG_ENABLED = True


SPIDER_MODULES = ['AreaForecast.spiders']
NEWSPIDER_MODULE = 'AreaForecast.spiders'

ITEM_PIPELINES = {
	#'CompanyPollution_lca.pipelines.CompanypollutionLcaPipeline': 100,
	#'CompanyPollution_lca.pipelines.CompanyInfoPipeline':150,
	'AreaForecast.pipelines.AreaforecastPipeline':100,
}
#SPIDER_MIDDLEWARES = {
#        'CompanyPollution_lca.spidermiddleware.DataSpiderMiddleware': 100, 
#}
#EXTENSIONS = {
#    'CompanyPollution_lca.logextension.SpiderOpenItemCloseLogging': 200,
#}
DOWNLOAD_DELAY = 1.2
DOWNLOAD_TIMEOUT = 400
USER_AGENT = "YisouSpider"
# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'CompanyPollution_lca (+http://www.yourdomain.com)'

if helper.get_pc_name() not in helper.ali_server:
    del(LOG_LEVEL)
    pass
