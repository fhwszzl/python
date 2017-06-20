from xml.dom import minidom
from math import radians, cos, sin, asin, sqrt
import numpy as np
import sys
#增加迭代深度
sys.setrecursionlimit(1000000)
#计算两点经纬度的距离
def haversine(lon1, lat1, lon2, lat2):  # 经度1，纬度1，经度2，纬度2 （十进制度数）
   """ 
   Calculate the great circle distance between two points  
   on the earth (specified in decimal degrees) 
   """
   # 将十进制度数转化为弧度
   lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
   # haversine公式
   dlon = lon2 - lon1
   dlat = lat2 - lat1
   a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
   c = 2 * asin(sqrt(a))
   r = 6371  # 地球平均半径，单位为公里
   return c * r

#通过筛选出距离的最小值的得到其索引，在通过索引得到城市名称
def WhereIAm(longitude_input,latitude_input,distance_list,province_name_list,city_name_list):
    """ 
中国东西距离5000km，南北距离5500公里
最北端在黑龙江省漠河乌苏里浅滩黑龙江主航道中心线上（53°33′N,122°37′E）.
最南端在南海的南沙群岛中的立地暗沙（3°51′N,112°16′E）（在曾母暗沙西南约15海里）.
最东端在黑龙江省黑瞎子岛(48°27′N,135°05′E）.
最西端在新疆帕米尔高原,约在中、塔、吉三国边界交点西南方约25公里处,那里有一座海拔5000米以上的雪峰.（39°15′N、73°33′E）.
    """
    longitude = list([112.16, 135.05, 73.33, 122.37])
    latitude = list([3.51,48.27,39.15,53.33])
    x1=haversine(longitude_input,latitude_input,float(longitude[0]),float(latitude[0]))
    x2=haversine(longitude_input,latitude_input,float(longitude[1]),float(latitude[1]))
    x3=haversine(longitude_input,latitude_input,float(longitude[2]),float(latitude[2]))
    x4=haversine(longitude_input,latitude_input,float(longitude[3]),float(latitude[3]))
    distance_avg = (x1+x2+x3+x4)/4
    if(distance_avg)>5500:
        print("国外")
        exit(0)
    else:
        min_value = find_min(distance_list)
        i = distance_list.index(min_value)
        print(province_name_list[i]+" - "+city_name_list[i])

#算出距离列表中的最小值
def find_min(distance_list):
    min_value = distance_list[0]
    if len(distance_list) ==1:
        return min_value
    else:
        tmp = find_min(distance_list[1:])
        if tmp <min_value:
            min_value = tmp
    return min_value



# 使用minidom解析器打开 XML 文档
DOMTree = minidom.parse("ChinaLocation.xml")
country = DOMTree.documentElement
x = input("please input ：")
lstValues = x.split(",")
#通过键盘得到经纬度
longitude_input = float(lstValues[0])
latitude_input  = float(lstValues[1])
#通过读取xml中的值封装成三个列表
distance_list=list()
province_name_list=list()
city_name_list=list()
# 在集合中获取所有省份
provinces = country.getElementsByTagName("provinces")
# 打印每个省份的城市的详细信息
for province in provinces:
   if province.hasAttribute("name"):
    for city in province.getElementsByTagName("city"):
     longitude = float(city.getAttribute("longitude"))
     latitude = float(city.getAttribute("latitude"))
     province_name = province.getAttribute("name")
     city_name = city.getAttribute("name")
     distanc = haversine(longitude, latitude, longitude_input, latitude_input)
     province_name_list.append(province_name)
     city_name_list.append(city_name)
     distance_list.append(distanc)

WhereIAm(longitude_input,latitude_input,distance_list,province_name_list,city_name_list)
