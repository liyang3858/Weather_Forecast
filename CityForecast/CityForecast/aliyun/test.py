#! /bin/python
# -*- coding:utf-8 -*-

from ots2 import *
from OTSConfig import ots_config

ots_config = dict(ots_config)

ENDPOINT = ots_config["END_POINT"]
ACCESSID = ots_config["ACCESS_KEY_ID"]
ACCESSKEY = ots_config["ACCESS_KEY_SECRET"]
INSTANCENAME = ots_config["INSTANCE_NAME"]

from ots2 import *

def main():
	ots_client = OTSClient(ENDPOINT, ACCESSID, ACCESSKEY, INSTANCENAME)

	#describe table
	describe_response = ots_client.describe_table('airqualityinfo_hourly_citylevel')
	print(u"表的名称: %s" % describe_response.table_meta.table_name)
	print(u"表的主键：%s" % describe_response.table_meta.schema_of_primary_key)
	print(u"表的预留读吞吐量：%s" % describe_response.reserved_throughput_details.capacity_unit.read)
	print(u"表的预留写吞吐量：%s" % describe_response.reserved_throughput_details.capacity_unit.write)
	print(u"最后一次上调预留读写吞吐量的时间：%s" % describe_response.reserved_throughput_details.last_increase_time)
	print(u"最后一次下调预留读写吞吐量的时间：%s" % describe_response.reserved_throughput_details.last_decrease_time)
	print(u"UTC自然日内总的下调预留读写吞吐量次数：%s" % describe_response.reserved_throughput_details.number_of_decreases_today)

if __name__ == '__main__':
	main()
