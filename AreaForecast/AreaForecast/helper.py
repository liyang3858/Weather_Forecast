# -*-coding:utf-8-*-
#-------------------------
# author: lca
# start_time: 20161010
#-------------------------
''' ''' ''' ''' ''' ''' '''
 whichEncode               判断字符编码
 get_uuid                  利用 uuid3 生成某个名称对应的uuid字符串
 get_element_of_list       从xpath得到的list中，获取list的内容
 str2time                  将时间字符串转化为10位时间戳字符串
 city2code                 将一个城市/区转换为对应的id
 citycode2id               将一个行政代码转化为对应的id
 code2parent               将一个城市代码转换为父节点信息
 find_longitude_latitude   识别经纬度并转化为°(度的小数形式),可以传两个字符串：纬度一个字符串、经度一个字符串，也可以传一个字符串：纬度经度
 get_pc_name               获取本机的名称
 get_now                   返回当前时间 2016-11-18 14:37:18, 或者传递一个代表小时的数字x，返回距今x小时的时刻
 last_3_days               给定一个时间字符串或者时间戳或者时间戳字符串，判断是否是最近2天的时间
 pollutant2code            根据污染物名称，返回国标中的编码
 sleep_random1             休眠 1以内的随机秒数
 coordinate2standard       将不规范坐标转化为数字与点的连接
 parseQuarter              将"2016年 第1季度" 转换成本季度最后一天2016-03-31 00:00:00
 parseMonth                将“2016年 5月”转成2016-05-31 00:00:00， 本月最后一天
 parseWeek                 将"2016年 第50周" 转换成 2016-12-12 00:00:00， 本周最后一天
 out_date                  根据一年中的第几天判断出日期 print out_date(2016,221)       #2016-08-08
 in_5_days                 判断是否是过去5天之内，time为时间字符串，在五天内返回 true
 on_5_days                 判断是否是过去第5天，time为时间字符串,在五天内返回 true
 get_SW_path               给出一个软件的名称(默认phantomjs),返回他的路径,若无,则返回 ''
 unit_conversion           单位转换的函数，给定 一个单位 和 一个值， 返回转化为标准单位(我们的约定标准)所对应的值
 get_scale_code            根据企业规模返回企业规模代码


 变量
 ali_server			ali服务器的名字
 pollutant			污染物对照表
 guokongtype                    国控类型
 MAX_CONNECTION_NUM             阿里云mysql的最大连接数

''' ''' ''' ''' ''' ''' '''

import sys
import re
import time
import datetime
import database

reload(sys)
sys.setdefaultencoding('utf-8')

MAX_CONNECTION_NUM = 50
ali_server = ["iZ28n6jmz8kZ",]
test_server = ["ThEnv-TestGround",]
guokongtype = {u"国控废气":2, u"国控废水":1, u"污水处理厂":3, u"重金属企业":4, u"畜牧养殖场":5, u"危险废物企业":6, u"农垦总局":7}
pollutant = {u"烟气流量":"a01999", u"水流量":"w01999", 'pH':'w01001', u'pH值':'w01001', u'PH值':'w01001', 'PM10':'a34002', u'氨':'a21001', u'氨氮':'w21003', u'苯':'w25002', u'苯胺类':'w26001', u'苯并(a)芘':'a25044', u'苯并(A)芘':'a25044', u'苯并（a）芘':'a25044', u'苯可溶物':'a25040', u'粪大肠菌群':'w02003', u'氮氧化物':'w02003', u'动植物油':'w22002', u'多环芳烃':'w25041', u'二噁英':'a25073', u'二氧化氮':'a21004', u'二氧化硫':'a21026', u'二氧化氯':'a21023', u'非甲烷总烃':'a24088', u'酚类':'w23001', u'粪大肠菌群数':'w02003', u'氟化氢':'a21006', u'氟化物':'w21017', u'高锰酸盐指数':'w01019', u'铬':'w20116', u'镉':'w20115', u'镉及化合物':'w20115', u'汞':'w20111', u'汞及化合物':'w20111', u'化学需氧量':'w01018', u'挥发酚':'w23002', u'挥发性酚类':'w23002', u'浑浊度':'浑浊度', u'活性氯':'w21023', u'甲醇':'w30001', u'颗粒物':'a34000', u'可吸附有机卤素化合物（AOX）':'w99002', u'沥青烟':'a34038', u'林格曼黑度':'a01010', u'硫化氢':'21028', u'硫化物':'w21019', u'硫酸盐':'w21038', u'六价铬':'w20117', u'铝':'w20002', u'氯化氢':'a21024', u'氯化物':'w21022', u'氯气':'a21022', u'氯乙烯':'a24046', u'煤尘':'a34028', u'锰':'w20124', u'镍及化合物':'w20121', u'铅':'w20120', u'铅及化合物':'w20120', u'氰化氢':'a21021', u'氰化物':'w21016', u'氰化物（总氰化合物）':'w21016', u'全盐量':'w01008', u'溶解性沉固体':'w01006', u'色度':'w01002', u'砷':'w20119', u'砷及其化合物':'w20119', u'生化需氧量':'w01017', u'石油类':'w22001', u'锑及其化合物':'w20004', u'铁':'w20125', u'铜':'w20122', u'烷基汞':'w20113', u'温度':'a01001', u'五日生化需氧量':'w01017', u'锡及化合物':'w20092', u'细菌总数':'w02006', u'硝基苯类':'w25023', u'硝酸盐':'w21007', u'锌':'w20123', u'悬浮物':'w01012', u'亚硝酸盐':'w21006', u'烟尘':'a34013', u'一氧化碳':'a21005', u'阴离子表面活性剂（LAS）':'w19002', u'总大肠菌群':'w02004', u'总氮':'w21001', u'总铬':'w20116', u'总镉':'w20115', u'总汞':'w20111', u'总钴':'w20038', u'总磷':'w21011', u'总锰':'w20124', u'总镍':'w20121', u'总铅':'w20120', u'总砷':'w20119', u'总铁':'w20125', u'总铜':'w20122', u'总锌':'w20123', u'总悬浮颗粒物':'a34001', u'总悬浮颗粒物（TSP）':'a34001', u'总银':'w20126', u'总硬度(以CaCO3计)':'w01007', u'昼间L10':'nxx041', u'夜间L10':'nxx042', u'昼间L50':'nxx051', u'夜间L50':'nxx052', u'昼间L90':'nxx061', u'夜间L90':'nxx062', u'昼间Leq':'nxx021', u'夜间Leq':'nxx022', 'Ld':'nxx021', 'Ln':'nxx022', u'昼间Lmax':'nxx031', u'夜间Lmax':'nxx032', u'二氧化氯':'a21023'}

def key_replace(key_list):
    # give a key_list and return a list in which the key is in list pollutant.
    i = -1

    for each_key in key_list:
        i += 1
        
        each_key = each_key.replace("(", "")
        each_key = each_key.replace(")", "")
        each_key = each_key.replace("（", "")
        each_key = each_key.replace("）", "")

        key_list[i] = each_key

        if each_key in pollutant.values():
            continue
        if each_key.upper() in pollutant or each_key == u"监测点位" or each_key == u"监测日期":
            continue

        new_key_list = key_judgement(each_key)
        
        if len(new_key_list) < 2: #粪大肠杆菌群数--->粪大肠杆菌群

            for pollutant_key in pollutant.keys(): # this is the most common method which can replace the method "key_judgement", but it may be very inefficient
                if pollutant_key == "":
                    continue
                if pollutant_key in each_key and pollutant_key != each_key:
                    print each_key + " is replaced by " + pollutant_key
                    key_list[i] = pollutant_key
                    break

            #pollutant[key_list[i]]# raise key error
            continue

        j = 0
        for each_new_key in new_key_list:
            j += 1

            if each_new_key in pollutant:
                print key_list[i] + " is repalced by " + each_new_key
                key_list[i] = each_new_key
                break
            elif j == len(new_key_list):
                #pollutant[key_list[i]]# raise key error
                pass

    return key_list

def get_uuid(name, namespace="tsinghua"): 
    # to get uuid from a name of a company or monitor(unicode), need 'import uuid' & 'import hashlib | import md5'

    md5 = __import__("md5")
    uuid = __import__("uuid")
    m = md5.new()
    m.update(namespace)
    namespace = uuid.UUID("{" + m.hexdigest() + "}")

    try:
        name = name.encode("utf8")
    except UnicodeDecodeError:
        pass

    return str(uuid.uuid3(namespace, name)).replace('-','')

def get_element_of_list(alist):
    # to get the data of a list from xpath.extract()
    return alist[0] if len(alist)>0 else ""

def str2time(time_str=None):
    # give a string of time and return the string of timestamp, if nothing is given, return the string of now
    time = __import__("time")
    datetime = __import__("datetime").datetime
    this_year_last_2 = datetime.today().year % 100
    this_year_first_2 = datetime.today().year / 100

    if time_str:
        if time_str.find(":") == -1:
            time_str += " 0:0:0"

    if not time_str:
        time_obj = time.localtime(time.time())

    elif time_str.find("/") != -1:
        # judge that the length of year is 2 or 4, if 2, modify it
        time_list = time_str.split("/")
        year = time_list[0]

        if len(year) == 2 and ( int(year) > this_year_last_2 ):
                time_list[0] = "19" + year
        elif len(year) == 2:
            time_list[0] = str(this_year_first_2) + year

        time_str = '/'.join(time_list)

        try:
            time_obj = time.strptime(time_str, '%Y/%m/%d %H:%M:%S')
        except ValueError, reason:
            if 'does not match format' in str(reason):
                time_obj = time.strptime(time_str, '%Y/%m/%d %H:%M')
            else:
                raise reason
        except Exception, reason:
            raise reason

    elif time_str.find("-") != -1:
        # judge that the length of year is 2 or 4, if 2, modify it
        time_list = time_str.split("-")
        year = time_list[0];

        if len(year) == 2 and ( int(year) > this_year_last_2 ):
            time_list[0] = "19" + year
        elif len(year) == 2:
            time_list[0] = str(this_year_first_2) + year

        time_str = '-'.join(time_list)#; print time_str

        try:
            time_obj = time.strptime(time_str, '%Y-%m-%d %H:%M:%S')
        except ValueError, reason:
            if 'does not match format' in str(reason):
                time_obj = time.strptime(time_str, '%Y-%m-%d %H:%M')
            else:
                raise reason
        except Exception, reason:
            raise reason
    # 时间格式错误
    if 'time_obj' not in dir():
        raise Exception("Wrong time form: " + time_str[:-6])

    return str(time.mktime(time_obj))[0:-2]

def city2code(city_district_name, province_city_name):
    '''
        give a name of a city/district and return the id of the city/district(cid)
        @input string_unicode_utf8  city_district_name  name of city or district, e.g.  晋城市、朝阳区
        @input string_unicode_utf8  province_city_name  name of province or city, e.g.  山西省、北京市
               province_city_name should be the parent of city_district_name in mysql. e.g. (city_district_name='太原市', province_city_name='山西省') or (city_district_name='杏花岭区', province_city_name='太原市') or (city_district_name='阳曲县', province_city_name='太原市')
        @output int id of the city or province(if not find the city) , or 0 if sometings wrong with the input
    '''
    import traceback
    import sqlite3
    import os

    try:
        city_district_name = city_district_name.decode("utf8")
        province_city_name = province_city_name.decode("utf8")
    except UnicodeDecodeError:
        pass

    #统一名称
    province = [u"北京市", u"天津市", u"河北省", u"山西省", u"内蒙古自治区", u"辽宁省", u"吉林省", u"黑龙江省", u"上海市", u"江苏省", u"浙江省", u"安徽省", u"福建省", u"江西省", u"山东省", u"河南省", u"湖北省", u"广东省", u"广西壮族自治区", u"海南省", u"重庆市", u"四川省", u"贵州省", u"云南省", u"西藏自治区", u"陕西省", u"甘肃省", u"青海省", u"宁夏回族自治区", u"新疆维吾尔自治区", u"香港特别行政区", u"澳门特别行政区", u"台湾省"]

    for province_each in province:
        if province_city_name in province_each:
            province_city_name = province_each

    db_path = os.path.dirname(os.path.abspath(__file__)) + '/city.db'

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    sql = '''select c1.`id`,c2.`id`,c3.`id` from polls_city c1 
             left join polls_city c2 on c1.parentid_id=c2.id
             left join polls_city c3 on c2.parentid_id=c3.id
             where c1.`name`=?
          '''

    rows1 = cursor.execute(sql, (city_district_name,))
    rows1 = cursor.fetchall()
    rows2 = cursor.execute(sql, (province_city_name,))
    rows2 = cursor.fetchall()

    rows1_len = len(rows1)
    rows2_len = len(rows2)

    try:
        #什么也没找到
        if rows2_len == 0:
            raise Exception("Cann't find %s in mysql!" % province_city_name)
        #找到了多个重名的市，报错。因为目前国内没有重复的市(level=3)
        if rows2_len > 1:
            raise Exception("Wrong to find more than 1 cities or pronvinces with %s!" % province_city_name)

        #没有找到 相应的市/区，返回相应的省/市id
        if rows1_len == 0:
            pass
        else:#至少找到了一个rows1
            #逐个判断是否为rows2的子节点
            for row1 in rows1: 
                for c_id in row1:
                    # 1表示全国，需排除
                    if c_id == 1:
                        continue

                    # c_id在rows2[0]中表示该项为rows2的子节点
                    if c_id in rows2[0]:
                        return row1[0]

        return rows2[0][0]
    except:
        traceback.print_exc()
        return 0
    finally:
        conn.close()

def citycode2id(citycode):
    '''
        give a code of a city/district and return the id of the city/district(cid)
        @input  string  citycode  code of province or city, e.g.  660600
        @output int     id of city in mysql. If not find , return highter level city/province of id which the city is in.
    '''
    import traceback
    import sqlite3
    import os

    db_path = os.path.dirname(os.path.abspath(__file__)) + '/city.db'

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    sql = '''select `id` from polls_city 
             where `code`=?
          '''
    rows_len = 0
    citycode_tmp = citycode
    i = 0 # when i=1, citycode = citycode[0:3] + "000", when i=2, citycode=citycode[0:2] + "0000" 
          # 以此来逐步提升citycode的level，从而避免未找到的code
    
    try:
        #没有找到 相应的市/区
        while rows_len == 0:
            i += 1

            rows = cursor.execute(sql, (citycode,))
            rows = cursor.fetchall()
            rows_len = len(rows)

            if i == 1:
                citycode = citycode[0:3] + "000"
            elif i == 2:
                citycode = citycode[0:2] + "0000"
            elif i == 3:# level为省
                pass
            else:
                raise Exception("Cann't find %s in mysql!" % citycode_tmp)

        return rows[0][0]

    except:
        traceback.print_exc()
        return 0
    finally:
        conn.close()

def city2code_old(city_district_name, province_city_name):
    '''
        give a name of a city/district and return the id of the city/district(cid)
        @input city_district_name  name of city or district, e.g.  晋城市、朝阳区
        @input province_city_name  name of province or city, e.g.  山西省、北京市
        province_city_name should be the parent of city_district_name in mysql. e.g. (city_district_name='太原市', province_city_name='山西省') or (city_district_name='杏花岭区', province_city_name='太原市') or (city_district_name='阳曲县', province_city_name='太原市')
    '''
    try:
        city_district_name = city_district_name.encode("utf8")
        province_city_name = province_city_name.encode("utf8")
    except UnicodeDecodeError:
        pass

    province_city_name = province_city_name.replace("省","")

    if province_city_name == "新疆":
        province_city_name = "新疆维吾尔自治区"

    MysqlClient = database.MysqlClient()

    if get_pc_name() in ali_server:
        MysqlClient.connect("mysql_insert_ali")
    else:
        MysqlClient.connect("mysql");

    sql = "SELECT `level`,`id`,`code`,`name` FROM polls_city where `name` LIKE %s"
    data_city_district = (city_district_name + "%",)
    data_province_city = (province_city_name + "%")

    rows = MysqlClient.query(sql, data_city_district)
    rows_province_city = MysqlClient.query(sql, data_province_city)
    len_r = len(rows)
    len_rp = len(rows_province_city)

    if len_rp == 0:
        raise Exception("Cann't find " + province_city_name + "in mysql!")
    else:
        top_level = rows_province_city[0]['level']

    if len_r == 0:
        cid = city2code(province_city_name, province_city_name)
    if len_r == 1:
        code = rows[0]['code']
        cid = rows[0]['id']
    else:#num of the set is two or more
        cid = city2code(province_city_name, province_city_name)

        for i in range(0, len_r):
            parent = rows[i]

            while int(parent['level']) != top_level:
                parent = code2parent(parent['code'], MysqlClient)

            if province_city_name in parent['name']:
                code = rows[i]['code']
                cid = rows[i]['id']
                break

    MysqlClient.close()
    return int(cid)

def code2parent(city_code, MysqlClient):
    #give a code of a city and retun the parent of it
    if city_code == 0:
        return 0

    sql = "SELECT `id`,`name`,`level`,`code`,`parentid_id` FROM polls_city WHERE `code` = %s"
    data = (city_code,)
    rows = MysqlClient.query(sql, data)

    if len(rows) == 1:
        result_this = rows[0]
    else: #cann't find
        result_this = {'code':0, 'parentid_id':1, 'name':'', 'level':1}

    sql = "SELECT `id`,`name`,`level`,`code` FROM polls_city WHERE `id`=%s"
    data = (result_this['parentid_id'],)
    rows = MysqlClient.query(sql, data) 
    result = rows[0]

    return result

def last_3_days(timestamp):
    time = __import__("time")

    if not isinstance(timestamp, int):
        timestamp = int(timestamp)

    return abs(time.time() -timestamp) < (2*24*60*60)

def find_longitude_latitude(text, text1=""):
    # if the length of result of text is 1, then we find pattern in text1
    re = __import__("re")

    pattern = re.compile(ur'(?P<degree>\d+)[\u5ea6\xb0\.](?P<minute>\d+)[\u5206\u2032\.](?P<second>\d+)?')
    match = re.findall(pattern ,text)
    match1 = re.findall(pattern, text1)

    match += match1

    longitude = 0
    latitude = 0

    for each_coor in match:
        i = 0
        temp = 0
        for each_d in each_coor:
            i += 1
            if each_d == "":
                each_d = 0
            each_d = float(each_d)

            if i == 2:#minute
                each_d /= 60
            if i == 3:#second
                each_d /= 3600

            temp += each_d

        if temp >90:
            longitude = temp
        else:
            latitude = temp

    return (longitude, latitude)

def get_pc_name():
    socket = __import__("socket")
    return  socket.getfqdn(socket.gethostname(  ))

def get_now(Hour=0):
    # gives an Hour and return the datetime before present
    datetime = __import__("datetime").datetime
    time = __import__("time")
    if isinstance(Hour, str):
        if Hour.isdigit():
            Hour = int(Hour)
        else:
            try:
                Hour = float(Hour)
            except ValueError,reason:
                if "could not convert string to float" in str(reason):
                    Hour = 0
    elif not (isinstance(Hour, int) or isinstance(Hour, float)):
        raise Exception("Type of the parameter is not correct!")

    if Hour == 0:#compatibility
        return str(datetime.now())[0:-7]
    else:
        now_timestamp = time.time()
        wanted_timestamp = now_timestamp - Hour * 60 * 60
        return time.strftime("%Y-%m-%d %H:%M:%S" ,time.localtime(wanted_timestamp))
        
def key_judgement(key):
    # input the string of the key of pollutant (unicode), return a list of the new key string
    # 总磷TP => [总磷, TP]
    
    if key == "":
        return []
    
    key0 = key[0].encode("utf8")
    key_isalnum = key[0].encode("utf8").isalnum()
    pos = -1
    
    for each_s in key:
        pos += 1
        
        if each_s.encode("utf8").isalnum() != key_isalnum:
            break

    if pos == len(key)-1:
        return [key]
    else :
        return [key[0:pos], key[pos:]]

def key_replace(key_list):
    # give a key_list and return a list in which the key is in list pollutant.
    i = -1

    for each_key in key_list:
        i += 1
        
        each_key = each_key.replace("(", "")
        each_key = each_key.replace(")", "")
        each_key = each_key.replace("（", "")
        each_key = each_key.replace("）", "")

        key_list[i] = each_key

        if each_key in pollutant.values():
            continue
        if each_key.upper() in pollutant or each_key == u"监测点位" or each_key == u"监测日期":
            continue

        new_key_list = key_judgement(each_key)
        
        if len(new_key_list) < 2: #粪大肠杆菌群数--->粪大肠杆菌群
            
            j = -1

            for pollutant_item in pollutant.items(): # this is the most common method which can replace the method "key_judgement", but it may be very inefficient
                pollutant_key = pollutant_item[0]
                pollutant_value = pollutant_item[1]

                if pollutant_key == "":
                    continue
                if pollutant_key in each_key and pollutant_key != each_key:
                    print each_key + " is replaced by " + pollutant_key
                    key_list[i] = pollutant_key
                    break

            #pollutant[key_list[i]]# raise key error
            continue

        j = 0
        for each_new_key in new_key_list:
            j += 1

            if each_new_key in pollutant:
                print key_list[i] + " is repalced by " + each_new_key
                key_list[i] = each_new_key
                break
            elif j == len(new_key_list):
                #pollutant[key_list[i]]# raise key error
                pass

    return key_list

def pollutant_2_item_keys():
    item_key = pollutant.values()
    item_key_limit = map(lambda x:x+"_limit", item_key)
    item_key_value = map(lambda x:x+"_value", item_key)
    return ',' + ','.join(item_key_limit) + ',' + ','.join(item_key_value)

def sleep_random1():
    sleep = __import__("time").sleep
    random = __import__("random").random
    sleep(random())

def coordinate2standard(coor_string):
    pattern = re.compile(r'\d+')
    coor = pattern.finditer(coor_string)

    abc = []
    for m in coor:
        abc.append(m.group())
        
    if len(abc) <= 1:
        return abc[0]
    return '.'.join([abc[0], abc[1]])

def get_scale_code(company_scale):
#输入企业规模是汉字描述 获得相应代码

    scale_dic = {u'特大型':'1', u'特大型企业':'1', u'大型一档':'2', u'大一型':'2', u'大型二档':'3', u'大二型':'3', u'中型一档':'4', u'中一型':'4', u'中型二档':'5', u'中二型':'5', u'小型':'6', u'小型企业':'6', u'其他':'7'}

    if company_scale in scale_dic:
        scale_code = scale_dic[company_scale]
    else:
        scale_code = '7'

    return scale_code

def parseQuarter(str):
    myre = '(\d{4})年\s第(\d+)季度'
    parttern = re.compile(myre, re.S)
    m = re.findall(parttern, str.encode("utf-8"))
    if m :
        year    = int(m[0][0])
        quarter = int(m[0][1])
        month = quarter * 3 +1
        if month >= 13:
            month = 1
            year = year + 1
        lastDay = datetime.datetime(year, month , 01)  - datetime.timedelta(days=1)
        return lastDay

def parseMonth(str):
    myre = '(\d{4})年\s(\d+)月'
    parttern = re.compile(myre, re.S)
    m = re.findall(parttern, str.encode("utf-8"))
    if m :
        year  = int(m[0][0])
        month = int(m[0][1])
        if month == 12 :
            year = year +1
            month = 1
        else:
            month = month + 1
        lastDay = datetime.datetime(year, month , 01)  - datetime.timedelta(days=1)
        return lastDay

def parseWeek(str):
    myre = '(\d{4})年\s第(\d+)周'
    parttern = re.compile(myre, re.S)
    m = re.findall(parttern, str.encode("utf-8"))
    if m :
        year = int(m[0][0])
        week = int(m[0][1])
        # 获得year第一天的星期数num，(0周一， 6周日)
        num =  datetime.datetime(year, 01 , 01).weekday()
        day =  7*(week-1) + 7-num
        dt = out_date(year, day)
        return dt + ' 00:00:00'

def out_date(year,day):
    fir_day = datetime.datetime(year,1,1)
    zone = datetime.timedelta(days=day-1)
    return datetime.datetime.strftime(fir_day + zone, "%Y-%m-%d")

def in_5_days(timeStr):
    timestamp = str2time(str(timeStr))
    if (time.time()-int(timestamp) < 5*24*60*60) and (time.time()-int(timestamp) > 0):
        return True
    else :
        return False

def on_5_days(timeStr):
    timestamp = str2time(str(timeStr))
    if (time.time()-int(timestamp) < 5*24*60*60) and (time.time()-int(timestamp) > 4*24*60*60):
        return True
    else:
        return False

def get_SW_path(SW='phantomjs'):
    ''' give a name of software (SW) and return the path of SW'''

    commands = __import__('commands')
    (status, output) = commands.getstatusoutput('whereis ' + SW)
    output = output.split(' ')
    path = output[1] if len(output)>1 else ''
    
    return path
def unit_conversion(unit_name, value):
    '''
    conversion of different unit to our standard unit
    @input unit_name: name of the unit you give
    @input value:     value of the unit you give
    @output : value of the standard unit,
              if unit_name you give is unknow, return the num of value you give
    '''
    if isinstance(value, str) or isinstance(value, unicode):
        value = eval(value)

    if isinstance(value, int) or isinstance(value, float) or isinstance(value, long):
        pass
    else:
        raise ValueError("value must be a number or a string of number! your value is " + value + " " + str(type(value)))

    # add new conversion in this dict
    conversion_dict = {1:"", 3600:'m3/s,l/s', 1000:'MPa'}
    
    conversion_key = conversion_dict.keys()
    count = len(conversion_dict)

    #unify the encoding
    try:
        unit_name = unit_name.decode("utf8")
    except UnicodeEncodeError:
        pass
    except UnicodeDecodeError:
        pass

    try:
        unit_name = unit_name.decode("gbk")
    except UnicodeEncodeError:
        pass
    except UnicodeDecodeError:
        pass

    #traverse to find unit_name in conversion_dict
    for multiple in conversion_key:
        if unit_name in conversion_dict[multiple]:
            break;
        else:
            count -= 1

    # if count==0 (cann't find unit_name in conversion_dict) or unit_name==""
    multiple = [multiple ,1][int(count==0 or unit_name=="")]


    value = float(value)
    value *= multiple

    if value % 1 == 0:
        value = int(value)

    return str(value)

def pollutant2code(pollutant_item,pollutant_type=None):
    '''
    根据污染物名称，返回国标中的编码，中文名称需与国标pdf中的中文名称一致，或者直接运行pollutant.py得到所有的中文名称
    @input pollutant: 污染物名称
    @input pollutant_type: 污染物的类型，可取值为 'w','a','n'，分别表示水、气、噪声
                           若不给出pollutant_type，则会按照水、气、噪声的顺序查找污染物字典
                           若给出pollutant_type，则会优先查找相应类型的污染物代码
    @output 污染物编码，string
            未找到则返回''，并进行提示
    
    '''
    import pollutant as pollutant_dict

    pullutant_dict = pollutant_dict.pollutant

    try:
        pollutant_item = pollutant_item.decode("utf8")
    except UnicodeEncodeError:
        pass
    except UnicodeDecodeError:
        pass

    if pollutant_type:
        if pollutant_type not in ['w', 'a', 'n']:
            print "======================================"
            print "your pollutant_type is " + pollutant_type
            print "pollutant_type should be 'w' or 'a' or 'n'"
            print "======================================"
            return ''

    #简单判断排口类别 水 or 气 or 噪
    if pollutant_type == "w":
        p_d_d = ['w', 'a', 'n']
    elif pollutant_type == "a":
        p_d_d = ['a', 'w', 'n']
    else:
        p_d_d = ['n', 'a', 'w']

    count = 3

    for p_d in p_d_d:
        if not pullutant_dict[p_d].get(pollutant_item):
            count -= 1
        else:
            break

    if count == 0:
        print "new pollutant >>>>>>>> " + pollutant_item.decode("utf8") + " <<<<<<<<<<<<"
        return ""

    pollutant_id = pullutant_dict[p_d].get(pollutant_item)
            
    if not pollutant_id:
        print "new pollutant >>>>>>>> " + pollutant_item.decode("utf8") + " <<<<<<<<<<<<"
        return ""

    return pollutant_id

pollutant_old = {u'铜':'Cu', u'沥青烟':'asphalt_fume', u'总磷':'TP', u'NH3':'NH3', u'粪大肠菌群':'fecal_coliform', u'硫化物':'sulfide', u'氟化物':'fluoride', u'烟气流速':'flue_gas_velocity', u'恶臭':'odor', u'烟气湿度':'flue_gas_humidity', u'甲醛':'HCHO', u'NO':'NO', u'BP':'BP', u'COD':'COD', u'石油类':'petroleum', u'TOC':'TOC', u'pH':'PH', u'烟气压力':'flue_gas_pressure', u'二噁英':'dioxin', u'一氧化碳':'CO', u'总铬':'T_Cr', u'BOD生化需氧量':'BOD', u'挥发酚':'volatile_phenols', u'硫化氢':'H2S', u'废水流量':'wastewater_flow', u'镉及其化合物':'Cd', u'溶解氧':'DO', u'标况流量':'standard_flow', u'氨':'NH3', u'总汞':'T_Hg', u'活性氯':'active_chlorine', u'总铜':'T_Cu', u'二氧化硫':'SO2', u'总铁':'T_Fe', u'烟气温度':'flue_gas_temperature', u'NO2':'NO2', u'总铅':'T_Pb', u'水温':'water_temperature', u'五氧化二磷':'P2O5', u'总镉':'T_Cd', u'非甲烷总烃':'NMHC', u'阴离子表面活性剂':'LAS', u'总镍':'T_Ni', u'六价铬':'Cr6+', u'粉尘':'stive', u'总砷':'T_As', u'砷':'As', u'Pm10':'PM10', u'烟尘':'sulphur_dioxide', u'镍':'Ni', u'流量':'flow', u'锌':'Zn', u'氯乙烯':'C2H3Cl', u'铅及其化合物':'Pb', u'浊度（原003）':'turbidity', u'氨氮':'NH3-N', u'瞬时流量':'instantaneous_flow', u'硫酸雾':'sulfuric_acid_mist', u'累计流量4#':'integrated_flow', u'砷及其化合物':'As', u'氯气':'Cl2', u'总氮':'TN', u'氮氧化物':'NOx', u'烟气动压':'flue_gas_dynamic_pressure', u'动植物油':'animal_and_vegetable_oil', u'时隔流量':'time_interval_flow', u'汞及其化合物':'Hg', u'O2含量':'O2', u'厂界噪音':'factory_boundary_noise', u'颗粒物':'particle', u'氯化氢':'HCl', u'色度':'color', u'标态流量':'standard_flow', u'格林曼黑度':'Greenman_blackness', u'氰化物':'cyanide', u'悬浮物':'SS', u'累计流量5#':'integrated_flow', u'气流量':'gas_flow', u'总锌':'T_Zn', u'铅浓度':'lead_concentration', u'铬酸雾':'chromic_acid_mist' , u'生化需氧量BOD':'BOD', u'生化需氧量':'BOD', u'化学需氧量':'COD', u'COD化学需氧量':'COD', u'化学需氧量COD':'COD', u'PH值':'PH', u'油':'oil', u'烷基汞':'alkyl_mercury', u'厂界噪声(昼间)':'noise_day', u'厂界噪声(夜间)':'noise_night', u'总锰':'T_Mn', u'Leq昼':'Leq_day', u'Leq夜':'Leq_night', u'林格曼黑度':'Ringelmann_blackness', u'苯胺类':'aniline', u'邻-二甲苯':'o_xylene', u'大肠菌群数':'fecal_coliform', 'Lmax昼':'Lmax_day', u'Lmax夜':'Lmax_night', u'L50昼':'L50_day', u'L50夜':'L50_night', 'Ln':'noise_night', 'Ld':'noise_day', u'L10昼':'L10_day', u'L10夜':'L10_night', u'L90昼':'L90_day', u'L90夜':'L90_night', u'铍及其化合物': 'Be', u'臭气浓度无量纲':'odor', u'氧O2':'O2', u'温度':'flue_gas_temperature', u'湿度':'flue_gas_humidity', u'二甲苯':'o-xylene', u'工业粉尘':'stive', u'磷酸盐以P计':'phosphates', u'碳氢化合物含非甲烷总烃':'hydrocarbon', u'颗粒物炭黑尘、燃料尘':'particle', u'颗粒物其他':'particle', u'粪大肠菌群数':'fecal_coliform', u'硝基苯类':'nitrobenzene', u'三甲胺':'trimethylamine', u'甲硫醇':'methyl_mercaptan', u'甲硫醚':'dimethyl_sulfide', u'氯化物':'chloride', u'苯C6H6':'benzene', u'二硝基甲苯DNT':'DNT', u'钼':'Mo', u'总氰':'cyanide', u'丙烯腈':'acrylonitrile', u'苯并a芘':'benzopyrene', u'锡及其化合物':'Sn', u'总银':'T_Ag', u'氟化物(气)':'fluoride', u'对-二甲苯':'para_xylene', u'甲苯':'methylbenzene', u'可吸附有机卤素':'AOX', u'液态氮':'LN', u'铬':'Cr', u'甲醇':'Methanol', u'磷酸化合物':'PO4', u'银':'Ag', u'苯胺':'Aniline', u'':'empty', u'总锑':'T_Sb', u'噪声(昼间)':'noise_day', u'噪声(夜间)':'noise_night'}

MonitorDataItem_attribute_cols_old = "monitoringmethod,COD_limit,COD_value,PH_limit,PH_value,admin_standard,andan_limit,andan_value,danyanghuawu_limit,danyanghuawu_value,eryanghualiu_limit,eryanghualiu_value,fuhuawu_limit,fuhuawu_value,liuliang_limit,liuliang_value,paishuiliang_limit,paishuiliang_value,yanchen_limit,yanchen_value,yangqihanliang_limit,yangqihanliang_value,yanqiliuliang_limit,yanqiliuliang_value,yanqiwendu_limit,yanqiwendu_value,yanqiyali_limit,yanqiyali_value,zongdan_limit,zongdan_value,zongge_limit,zongge_value,zonglin_limit,zonglin_value,zongshen_limit,zongshen_value,huaxuexuyangliang_value,huaxuexuyangliang_limit,wendu_value,wendu_limit,shenghuaxuyangliang_value,shenghuaxuyangliang_limit,qinghuawu_value,qinghuawu_limit,sedu_value,sedu_limit"
if __name__ == '__main__':
    #print key_judgement(u"O2含量")
    #print get_now(1)
    #print find_longitude_latitude(u'\u7ecf117\xb023\u203257\u2033 \u7eac39\xb053\u203258\u2033')
    #key_list = [u"化学需氧量(tgfbt)", "sdfasd"]
    #print key_replace((u"化学需氧量(COD)"))
    #print key_list
    #print get_SW_path('haha')
    #print city2code(u"哈密市",u"新疆")
    #print unit_conversion("", u'7.4647')
    #print str2time("fowiejfo")
    #print pollutant2code("氨氮")
    #print citycode2id("660600")
    #print get_uuid(u"河北旭阳焦化有限公司")
    print get_uuid(u'郑州裕中能源有限责任公司')
    pass

