import math
import osmnx as ox
import pandas as pd
import pickle
import networkx as nx
import time
import json
import random
import urllib #坐标系转换的时候有用

non_empty_taxi_set = set()

x_pi = 3.14159265358979324 * 3000.0 / 180.0
pi = 3.1415926535897932384626  # π
a = 6378245.0  # 长半轴
ee = 0.00669342162296594323  # 偏心率平方
ran = 0
def random_color():
    global ran
    rr = gg = bb = 60
    if ran == 0:
        rr = 195
    elif ran == 1:
        gg = 195
    else:
        bb = 195
    ran = (ran + 1)%3
    r = str(hex(round(rr + 60 * random.random())))[2:4]
    g = str(hex(round(gg + 60 * random.random())))[2:4]
    b = str(hex(round(bb + 60 * random.random())))[2:4]
    return '#' + r+g+b



def gcj02_to_bd09(lng, lat):#!!!
    z = math.sqrt(lng * lng + lat * lat) + 0.00002 * math.sin(lat * x_pi)
    theta = math.atan2(lat, lng) + 0.000003 * math.cos(lng * x_pi)
    bd_lng = z * math.cos(theta) + 0.0065
    bd_lat = z * math.sin(theta) + 0.006
    return [bd_lng, bd_lat]



def wgs84_to_gcj02(lng, lat): #!!!!
    dlat = _transformlat(lng - 105.0, lat - 35.0)
    dlng = _transformlng(lng - 105.0, lat - 35.0)
    radlat = lat / 180.0 * pi
    magic = math.sin(radlat)
    magic = 1 - ee * magic * magic
    sqrtmagic = math.sqrt(magic)
    dlat = (dlat * 180.0) / ((a * (1 - ee)) / (magic * sqrtmagic) * pi)
    dlng = (dlng * 180.0) / (a / sqrtmagic * math.cos(radlat) * pi)
    mglat = lat + dlat
    mglng = lng + dlng
    return [mglng, mglat]



def wgs84_to_bd09(lon, lat):
    lon, lat = wgs84_to_gcj02(lon, lat)
    return gcj02_to_bd09(lon, lat)


def _transformlat(lng, lat):
    ret = -100.0 + 2.0 * lng + 3.0 * lat + 0.2 * lat * lat + \
          0.1 * lng * lat + 0.2 * math.sqrt(math.fabs(lng))
    ret += (20.0 * math.sin(6.0 * lng * pi) + 20.0 *
            math.sin(2.0 * lng * pi)) * 2.0 / 3.0
    ret += (20.0 * math.sin(lat * pi) + 40.0 *
            math.sin(lat / 3.0 * pi)) * 2.0 / 3.0
    ret += (160.0 * math.sin(lat / 12.0 * pi) + 320 *
            math.sin(lat * pi / 30.0)) * 2.0 / 3.0
    return ret


def _transformlng(lng, lat):
    ret = 300.0 + lng + 2.0 * lat + 0.1 * lng * lng + \
          0.1 * lng * lat + 0.1 * math.sqrt(math.fabs(lng))
    ret += (20.0 * math.sin(6.0 * lng * pi) + 20.0 *
            math.sin(2.0 * lng * pi)) * 2.0 / 3.0
    ret += (20.0 * math.sin(lng * pi) + 40.0 *
            math.sin(lng / 3.0 * pi)) * 2.0 / 3.0
    ret += (150.0 * math.sin(lng / 12.0 * pi) + 300.0 *
            math.sin(lng / 30.0 * pi)) * 2.0 / 3.0
    return ret

    
print('载入Tool中')
map_file = open('mTshare/data/map.pickle', 'rb')
osm_map = pickle.load(map_file)  # osm地图, 在判断距离某个经纬点最近的道路节点时可以使用
req_to_taxi_map = {} # req的id映射到taxi的id

map_file.close()
tool_node_list = []
df = pd.read_csv('mTshare/data/node_list_with_cluster.csv')
tli = df.loc[:, 'real_id']
cluster_li = df.loc[:, 'cluster_id']
tmpp = [i for i in range(len(tli))]
tool_node_list = zip(tli, tmpp)
id_hash_map = dict(tool_node_list)


SYSTEM_INIT_TIME = time.time()
EARLIEST_TIME = 1477929720   # 预先从数据库中查询出最早时间
TIME_OFFSET = SYSTEM_INIT_TIME - EARLIEST_TIME


def rad(deg):
    return (deg / 180.0) * math.pi


def divide_group1():
    print()
    print("------------------------------------")


def divide_group2():
    print("------------------------------------")
    print()

def get_distance(lon1, lat1, lon2, lat2):
    EARTH_RADIUS = 6378.137
    rad_lat1 = rad(lat1)
    rad_lat2 = rad(lat2)
    a = rad_lat1 - rad_lat2
    rad_lon1 = rad(lon1)
    rad_lon2 = rad(lon2)
    b = rad_lon2 - rad_lon1
    ret = 2 * math.asin(math.sqrt(math.pow(math.sin(a / 2), 2) +
                                  math.cos(rad_lat1) * math.cos(rad_lat2) * math.pow(math.sin(b / 2), 2)))
    ret *= EARTH_RADIUS
    ret = round(ret * 10000) / 10000
    return ret * 1000


def check_in_which_partition(lon, lat):
    ret = ox.get_nearest_node(osm_map, (lat, lon))
    ret = id_hash_map[ret]
    ret = cluster_li[ret]
    return ret


def get_shortest_path_node(node1, node2):
    return nx.shortest_path(osm_map, source=node1, target=node2, weight='length')


def get_shortest_path_length(node1, node2):
    return nx.shortest_path_length(osm_map, source=node1, target=node2, weight='length')


# 余弦相似度
def cosine_similarity(vec1, vec2):
    x = [vec1[2]-vec1[0], vec1[3]-vec1[1]]
    y = [vec2[2]-vec2[0], vec2[3]-vec2[1]]
    result1 = 0.0
    result2 = 0.0
    result3 = 0.0
    for i in range(len(x)):
        result1 += x[i]*y[i]  # sum(X*Y)
        result2 += x[i]**2  # sum(X*X)
        result3 += y[i]**2  # sum(Y*Y)

    return result1/((result2*result3)**0.5)

# def cosine_similarity(vec1, vec2):
#     x = [vec1[0], vec1[1], vec1[2], vec1[3]]
#     y = [vec2[0], vec2[1], vec2[2], vec2[3]]
#     sum_xy = 0.0
#     normX = 0.0
#     normY = 0.0
#     for a, b in zip(x, y):
#         sum_xy += a * b
#         normX += a ** 2
#         normY += b ** 2
#     if normX == 0.0 or normY == 0.0:
#         return None
#     else:
#         tmp = sum_xy / ((normX * normY) ** 0.5)
#         return tmp
