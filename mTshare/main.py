import copy
import datetime
import glob
import json
import math
import os
import pickle
import random
import time

import numpy as np
import osmnx as ox
import pandas as pd
import pymysql
from tqdm import tqdm

from mTshare.MobilityVector import MobilityVector
from mTshare.Node import Node
from mTshare.Partition import Partition
from mTshare.Path import Path
from mTshare.Request import Request
from mTshare.Taxi import Taxi
from mTshare.Tool.Tool import *

# import sys

print('载入main.py中')


def system_init():
    print('System Initiating...')
    taxi_table = pd.read_csv('mTshare/data/taxi_info_list.csv')
    df = pd.read_csv('mTshare/data/node_list_with_cluster.csv')
    for indexs in df.index:
        tmp = df.loc[indexs]
        node_list.append(
            Node(tmp['real_id'], tmp['lon'], tmp['lat'], int(tmp['cluster_id'])))

    # .里面包含的内容是每个partition的landmark的经纬度.其下标与partition_list的下标一一对应
    landmark_table = pd.read_csv('mTshare/data/landmark.csv')
    global landmark_list
    landmark_list = list(
        zip(landmark_table.loc[:, 'lon'], landmark_table.loc[:, 'lat'], landmark_table.loc[:, 'landmark_node_id']))

    global partition_list
    partition_list = [None] * (max(df.loc[:, 'cluster_id']) + 1)
    # 初始化所有partition实例
    for node_it in node_list:
        cid = node_it.cluster_id_belongto
        if partition_list[cid] is None:
            partition_list[cid] = Partition(cid, node_list=[], taxi_list=[])
            partition_list[cid].node_list.append(int(node_it.node_id))
        else:
            partition_list[cid].node_list.append(int(node_it.node_id))

    global taxi_list
    for taxi_it in taxi_table.index:
        tmp = taxi_table.loc[taxi_it]
        taxi_in_which_partition = check_in_which_partition(
            tmp['init_lon'], tmp['init_lat'])
        taxi_list.append(
            Taxi(int(tmp['taxi_id']), tmp['init_lon'], tmp['init_lat'], SYSTEM_INIT_TIME - TIME_OFFSET, partition_id_belongto=taxi_in_which_partition, seat_left=3))
        partition_list[taxi_in_which_partition].taxi_list.append(
            int(tmp['taxi_id']))

    # 初始化邻接矩阵
    global node_distance_matrix
    node_distance_matrix = copy.copy(node_distance.values)


def request_fetcher(time_slot_start, time_slot_end):
    sql = "SELECT * FROM myorder WHERE  start_time between {} and {} AND start_longitude between 104.0299 and 104.1013 AND end_longitude between 104.0299 and 104.1013 AND start_latitude between 30.6364 and 30.6868 AND end_latitude between 30.6364 and 30.6868 ".format(
        time_slot_start, time_slot_end)
    cursor.execute(sql)
    ret = cursor.fetchall()
    return ret


def update(request):
    divide_group1()
    print('In update')
    global now_time
    aux_dict = {}
    print('req_to_taxi_map is {}'.format(req_to_taxi_map))

    for req_id in req_to_taxi_map.keys():
        if request_list[req_id].delivery_deadline > now_time:
            aux_dict[req_id] = req_to_taxi_map[req_id]
        else:
            del request_list[req_id]
    req_to_taxi_map.clear()
    for req_id in aux_dict.keys():
        req_to_taxi_map[req_id] = aux_dict[req_id]
    for taxi_it in taxi_list:
        taxi_it.update_status(now_time)
    mobility_cluster.clear()
    general_mobility_vector.clear()
    for idx, request_it in request_list.items():
        vec1 = [request_it.start_lon, request_it.start_lat,
                request_it.end_lon, request_it.end_lat]
        max_cos = -2
        max_idx = -1
        flag = False
        for idx, gene_it in enumerate(general_mobility_vector):
            cos_val = cosine_similarity(
                [gene_it.lon1, gene_it.lat1, gene_it.lon2, gene_it.lat2], vec1)
            # 计算出最相似的那个general_mobility_vector
            if cos_val > max_cos:
                max_idx = idx
                max_cos = cos_val
        if max_cos >= Lambda:
            flag = True
        if flag:
            mobility_cluster[max_idx].append(MobilityVector(
                vec1[0], vec1[1], vec1[2], vec1[3], 'REQ', request_it.request_id))
            x = y = z = w = 0
            for it in mobility_cluster[max_idx]:
                x += it.lon1
                y += it.lat1
                z += it.lon2
                w += it.lat2
            leng = len(mobility_cluster[max_idx])
            general_mobility_vector[max_idx] = MobilityVector(
                x / leng, y / leng, z / leng, w / leng, 'REQ', request_it.request_id)
        else:
            mobility_cluster.append([MobilityVector(
                vec1[0], vec1[1], vec1[2], vec1[3], 'REQ', request_it.request_id)])
            general_mobility_vector.append(MobilityVector(
                vec1[0], vec1[1], vec1[2], vec1[3], 'REQ', request_it.request_id))

    for taxi_it in taxi_list:
        vec2 = taxi_it.mobility_vector
        if vec2 == None or taxi_it.seat_left == taxi_it.capability:
            continue
        max_cos = -2
        max_idx = -1
        flag = False
        for idx, gene_it in enumerate(general_mobility_vector):
            cos_val = cosine_similarity(
                [gene_it.lon1, gene_it.lat1, gene_it.lon2, gene_it.lat2], [vec2.lon1, vec2.lat1, vec2.lon2, vec2.lat2])
            if cos_val > max_cos:
                max_cos = cos_val
                max_idx = idx
        if max_cos >= Lambda:
            flag = True
        if flag:
            print('136行在已有cluster里面增加了TAXI的mv~~~~~~~~~~~~~·')
            mobility_cluster[max_idx].append(MobilityVector(
                vec2.lon1, vec2.lat1, vec2.lon2, vec2.lat2, 'TAXI', taxi_it.taxi_id))
            x = y = z = w = 0
            for it in mobility_cluster[max_idx]:
                x += it.lon1
                y += it.lat1
                z += it.lon2
                w += it.lat2
            leng = len(mobility_cluster[max_idx])
            general_mobility_vector[max_idx] = MobilityVector(
                x / leng, y / leng, z / leng, w / leng, 'TAXI', taxi_it.taxi_id)
        else:
            print('163 行增加了新的m-cluster---')
            mobility_cluster.append(
                [MobilityVector(vec2.lon1, vec2.lat1, vec2.lon2, vec2.lat2, 'TAXI', taxi_it.taxi_id)])
            general_mobility_vector.append(MobilityVector(
                vec2.lon1, vec2.lat1, vec2.lon2, vec2.lat2, 'TAXI', taxi_it.taxi_id))

    # 重置partition
    global partition_list
    for par_it in partition_list:
        par_it.taxi_list.clear()
    for taxi_it in taxi_list:
        partition_list[taxi_it.partition_id_belongto].taxi_list.append(
            int(taxi_it.taxi_id))
    divide_group2()


def taxi_req_matching(req: Request):
    divide_group1()
    print('In taxi req matching')
    u_lon, u_lat = req.start_lon, req.start_lat
    v_lon, v_lat = req.end_lon, req.end_lat
    req_start_node = ox.get_nearest_node(osm_map, (u_lat, u_lon))
    nearest_start_id = ox.get_nearest_node(osm_map, (u_lat, u_lon))
    nearest_end_id = ox.get_nearest_node(osm_map, (v_lat, v_lon))
    delta_t = req.delivery_deadline - node_distance_matrix[id_hash_map[nearest_start_id]][id_hash_map[nearest_end_id]] / TYPICAL_SPEED - req.release_time
    # 得到搜索范围的半径
    search_range = delta_t * TYPICAL_SPEED
    search_range = max(search_range, 0)
    after_tranform = wgs84_to_bd09(u_lon, u_lat)
    send_info({'type': 'circle', 'content': {
              'lon': after_tranform[0], 'lat': after_tranform[1], 'range': search_range}})
    print('search range is {}'.format(search_range))
    partition_intersected = set()
    for idx, node_it in enumerate(node_list):
        if node_it.cluster_id_belongto in partition_intersected:
            continue
        dis = node_distance_matrix[id_hash_map[req_start_node]
                                   ][id_hash_map[node_it.node_id]]
        if dis <= search_range:
            partition_intersected.add(node_it.cluster_id_belongto)

    # 计算出PzLt
    taxi_in_intersected = []
    for it in partition_intersected:
        # partion对象中的taxi_list放的是taxi的id
        for taxi_it in partition_list[it].taxi_list:
            if taxi_list[taxi_it].is_available:
                # 全局的taxi_list中放的是taxi对象, 故taxi_list[taxi_it].taxi_id是taxi的id
                taxi_in_intersected.append(taxi_list[taxi_it].taxi_id)

    if len(taxi_in_intersected) == 0:  # 在规定时间内没有taxi能来，所以放弃订单
        return None, None, None                    # 放弃订单了
    vec = [req.start_lon, req.start_lat, req.end_lon, req.end_lat]
    max_cos = -2
    max_idx = -1
    for idx, gene_v in enumerate(general_mobility_vector):
        cos_val = cosine_similarity(
            [gene_v.lon1, gene_v.lat1, gene_v.lon2, gene_v.lat2], vec)
        print('余弦相似度是：{}'.format(cos_val))
        if cos_val > max_cos:
            max_cos = cos_val
            max_idx = idx
    '''
        cluster不可能为空
    '''
    # 计算出CaLt
    C = mobility_cluster[max_idx]
    C_li = []
    for it in C:
        if it.vector_type == 'TAXI':
            C_li.append(it.ID)
        else:
            print(req_to_taxi_map)
            if not it.ID in req_to_taxi_map:
                continue
            # 此时的类型为req
            C_li.append(req_to_taxi_map[it.ID])

    print('C_li is: ')
    print(C_li)

    best_candidate_taxi = set(taxi_in_intersected).intersection(set(C_li))  # 取交集, 计算出所有候选taxi的list
    secondary_candidate_non_empty_taxi = set(taxi_in_intersected).difference(best_candidate_taxi)
    secondary_candidate_empty_taxi = list()

    for taxi_id in secondary_candidate_non_empty_taxi:
        if taxi_list[taxi_id].is_empty():
            secondary_candidate_empty_taxi.append(taxi_id)

    secondary_candidate_non_empty_taxi = secondary_candidate_non_empty_taxi.difference(set(secondary_candidate_empty_taxi))

    best_candidate_taxi = list(best_candidate_taxi)
    secondary_candidate_non_empty_taxi = list(secondary_candidate_non_empty_taxi)
    divide_group2()
    return best_candidate_taxi, secondary_candidate_empty_taxi, secondary_candidate_non_empty_taxi
    # best_candidate_taxi是mv也符合的车，secondary_candidate_empty_taxi是能到达但mv不符合的空车，
    # secondary_candidate_non_empty_taxi是能到达但mv不符合的非空车


def insertion_feasibility_check(taxi_id, req: Request, pos_i, pos_j):  # 在前面插入
    print('In insertion feasibility check')
    req_start_node_id = req.start_node_id
    req_end_node_id = req.end_node_id

    pre_node_lon = (taxi_list[taxi_id].schedule_list[pos_i - 1])['lon']
    pre_node_lat = (taxi_list[taxi_id].schedule_list[pos_i - 1])['lat']
    pre_node_id = ox.get_nearest_node(osm_map, (pre_node_lat, pre_node_lon))

    aft_node_lon = (taxi_list[taxi_id].schedule_list[pos_i])['lon']
    aft_node_lat = (taxi_list[taxi_id].schedule_list[pos_j])['lat']
    aft_node_id = ox.get_nearest_node(osm_map, (aft_node_lat, aft_node_lon))

    ddl = 0
    dis = node_distance_matrix[id_hash_map[pre_node_id]][id_hash_map[req_start_node_id]
                                                         ] + node_distance_matrix[id_hash_map[req_start_node_id]][id_hash_map[aft_node_id]]
    req_id = (taxi_list[taxi_id].schedule_list[pos_i])['request_id']
    if (taxi_list[taxi_id].schedule_list[pos_i])['schedule_type'] == 'ARRIVAL':
        ddl = request_list[req_id].delivery_deadline
    elif (taxi_list[taxi_id].schedule_list[pos_i])['schedule_type'] == 'DEPART':
        ddl = request_list[req_id].pickup_deadline

    if (taxi_list[taxi_id].schedule_list[pos_i - 1])['arrival_time'] + node_distance_matrix[id_hash_map[pre_node_id]][id_hash_map[req_start_node_id]] / TYPICAL_SPEED > ddl:
        return False

    for i in range(pos_i, len(taxi_list[taxi_id].schedule_list)):
        req_id = (taxi_list[taxi_id].schedule_list[i])['request_id']
        ddl_ = 0
        if (taxi_list[taxi_id].schedule_list[i])['schedule_type'] == 'ARRIVAL':
            ddl_ = request_list[req_id].delivery_deadline
        elif (taxi_list[taxi_id].schedule_list[i])['schedule_type'] == 'DEPART':
            ddl_ = request_list[req_id].pickup_deadline

        tmp = (taxi_list[taxi_id].schedule_list[i])[
            'arrival_time'] + dis / TYPICAL_SPEED
        if tmp > ddl_:
            return False
        (taxi_list[taxi_id].schedule_list[i])['arrival'] += tmp

    pre_node_lon = (taxi_list[taxi_id].schedule_list[pos_j - 1])['lon']
    pre_node_lat = (taxi_list[taxi_id].schedule_list[pos_j - 1])['lat']
    pre_node_id = ox.get_nearest_node(osm_map, (pre_node_lat, pre_node_lon))

    aft_node_lon = (taxi_list[taxi_id].schedule_list[pos_j])['lon']
    aft_node_lat = (taxi_list[taxi_id].schedule_list[pos_j])['lat']
    aft_node_id = ox.get_nearest_node(osm_map, (aft_node_lat, aft_node_lon))

    ddl = 0
    dis = node_distance_matrix[id_hash_map[pre_node_id]][id_hash_map[req_end_node_id]
                                                         ] + node_distance_matrix[id_hash_map[req_end_node_id]][id_hash_map[aft_node_id]]
    req_id = (taxi_list[taxi_id].schedule_list[pos_j])['request_id']
    if (taxi_list[taxi_id].schedule_list[pos_j])['schedule_type'] == 'ARRIVAL':
        ddl = request_list[req_id].delivery_deadline
    elif (taxi_list[taxi_id].schedule_list[pos_j])['schedule_type'] == 'DEPART':
        ddl = request_list[req_id].pickup_deadline

    if (taxi_list[taxi_id].schedule_list[pos_j - 1])['arrival_time'] + node_distance_matrix[id_hash_map[pre_node_id]][id_hash_map[req_end_node_id]] / TYPICAL_SPEED > ddl:
        return False

    for i in range(pos_j, len(taxi_list[taxi_id].schedule_list)):
        req_id = (taxi_list[taxi_id].schedule_list[i])['request_id']
        ddl_ = 0
        if (taxi_list[taxi_id].schedule_list[i])['schedule_type'] == 'ARRIVAL':
            ddl_ = request_list[req_id].delivery_deadline
        elif (taxi_list[taxi_id].schedule_list[i])['schedule_type'] == 'DEPART':
            ddl_ = request_list[req_id].pickup_deadline

        tmp = (taxi_list[taxi_id].schedule_list[i])[
            'arrival'] + dis / TYPICAL_SPEED
        if tmp > ddl_:
            return False
        (taxi_list[taxi_id].schedule_list[i])['arrival'] += tmp

    return True


def partition_filter(node1, node2):  # 返回一个数组，组成元素是partition id
    # print('In partition filter')
    # 根据论文P7
    partition1 = check_in_which_partition(node1['lon'], node1['lat'])
    partition2 = check_in_which_partition(node2['lon'], node2['lat'])
    if partition1 == partition2:
        return [partition_list[partition1]]
    landmark1 = landmark_list[partition1]
    landmark2 = landmark_list[partition2]

    node1 = ox.get_nearest_node(osm_map, (landmark1[1], landmark1[0]))
    node2 = ox.get_nearest_node(osm_map, (landmark2[1], landmark2[0]))

    # lm1到lm2的travel cost
    cost_1to2 = node_distance_matrix[id_hash_map[node1]
                                     ][id_hash_map[node2]] / TYPICAL_SPEED
    forever_mobility_vector = [landmark1[0],
                               landmark1[1], landmark2[0], landmark2[1]]

    filtered_partition = []
    for idx, one_partition in enumerate(partition_list):
        if partition1 == idx:  # 如果指向起点的partition就跳过
            continue
        tmp_lm = landmark_list[idx]
        tmp_vec = [landmark1[0], landmark1[1], tmp_lm[0], tmp_lm[1]]
        # Travel direction rule 来自论文P7左栏
        if cosine_similarity(tmp_vec, forever_mobility_vector) < Lambda:
            continue
        # Travel cost rule
        tmp_node = ox.get_nearest_node(osm_map, (tmp_lm[1], tmp_lm[0]))
        cost_1totmp = node_distance_matrix[id_hash_map[node1]
                                           ][id_hash_map[tmp_node]] / TYPICAL_SPEED
        cost_tmpto2 = node_distance_matrix[id_hash_map[tmp_node]
                                           ][id_hash_map[node2]] / TYPICAL_SPEED
        if cost_1totmp + cost_tmpto2 <= (1 + partition_filter_param) * cost_1to2:
            filtered_partition.append((one_partition, cost_1totmp))

    filtered_partition.sort(key=lambda x: x[1])
    # 使filtered_partition里的元组根据cost_1totmp递增的顺序排列

    filtered_partition = [i[0] for i in filtered_partition]
    '''
        注意第一个partition是不是taxi所在的地方
        最后一个partition是不是终点的地方
        感觉要将第一个和最后一个地方换成确切的lon lat而不是partition
    
    '''
    # print('len of filtered_partition')
    # print(len(filtered_partition))
    if partition_list[partition1] not in filtered_partition:
        filtered_partition.append(partition_list[partition1])
    if partition_list[partition2] not in filtered_partition:
        filtered_partition.append(partition_list[partition2])

    # print('len of filtered_partition')
    # print(len(filtered_partition))

    return filtered_partition


def basic_routing(Slist, taxi_it):    # 根据论文P7
    # print('In basic routing')
    taxi_path = Path(now_time)
    sum_path_distance = 0
    for idx, s_node in enumerate(Slist):
        # if taxi_it == 0:
        #     for slist_it in Slist:
        #         print(slist_it)
        # print('length of Slist is')
        # print(len(Slist))
        if idx == len(Slist) - 1:
            break
        path_distance = 0
        filtered_partition = partition_filter(Slist[idx], Slist[idx+1])

        pre_subgraph_nodes = []
        for filtered_partition_item in filtered_partition:
            for node_it in filtered_partition_item.node_list:
                pre_subgraph_nodes.append(node_list[id_hash_map[node_it]].node_id)

        if taxi_it == 0 and idx == 0:
            # print('writing log')
            nodes_in_filtered_partition_lon_file = open('./mTshare/log/nodes_in_filtered_partition_lon_file.txt', 'w+')
            nodes_in_filtered_partition_lat_file = open('./mTshare/log/nodes_in_filtered_partition_lat_file.txt', 'w+')
            for nn in pre_subgraph_nodes:
                nodes_in_filtered_partition_lon_file.write('%f,\n' % node_list[id_hash_map[nn]].lon)
                nodes_in_filtered_partition_lat_file.write('%f,\n' % node_list[id_hash_map[nn]].lat)
            nodes_in_filtered_partition_lon_file.close()
            nodes_in_filtered_partition_lat_file.close()

        pre_subgraph = osm_map.subgraph(pre_subgraph_nodes)
        isolate_cnt = 0
        non_isolate_nodes = []
        for it in pre_subgraph.nodes:
            if nx.is_isolate(pre_subgraph, it):
                isolate_cnt += 1
            else:
                non_isolate_nodes.append(it)

        subgraph = osm_map.subgraph(non_isolate_nodes)
        subgraph = nx.MultiGraph(subgraph)
        # 此时得到的subgraph是没有孤立点, 但仍有多个连通分量的

        components = nx.connected_components(subgraph)
        to_remove_nodes = []
        for it in components:
            if len(it) < 5:
                to_remove_nodes += [x for x in it]
        subgraph.remove_nodes_from(to_remove_nodes)
        # 此时得到的subgraph是没有孤立点, 且只有一个连通分量

        start_node = ox.get_nearest_node(subgraph, (Slist[idx]['lat'], Slist[idx]['lon']))
        
        end_node = ox.get_nearest_node(subgraph, (Slist[idx + 1]['lat'], Slist[idx + 1]['lon']))
        # print('start_node is {}'.format(start_node))
        # if taxi_it == 0:
        #     print('start_node lon and lat is {}, {}'.format(node_list[id_hash_map[start_node]].lon, node_list[id_hash_map[start_node]].lat))
        # print('end_node is {}'.format(end_node))
        # if taxi_it == 0:
        #     print('end_node lon and lat is {}, {}'.format(node_list[id_hash_map[end_node]].lon, node_list[id_hash_map[end_node]].lat))

        tmp_list = nx.dijkstra_path(subgraph, source=start_node, target=end_node, weight='length')

        #############################################
        # if taxi_it == 0 and idx == 1:
        #     print('1->2 path')
        #     print(tmp_list)
        #############################################

        tmp_list = [Node(x, node_list[id_hash_map[x]].lon, node_list[id_hash_map[x]].lat,
                         node_list[id_hash_map[x]].cluster_id_belongto) for x in tmp_list]

        taxi_path.path_node_list += tmp_list
        path_distance = nx.dijkstra_path_length(subgraph, source=start_node, target=end_node, weight='length')

        Slist[idx + 1]['arrival_time'] = Slist[idx]['arrival_time'] + path_distance / TYPICAL_SPEED
        print("Slist[idx]['arrival_time'] is " + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(Slist[idx]['arrival_time'])))
        print("Slist[idx + 1]['arrival_time'] is " + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(Slist[idx + 1]['arrival_time'])))
        # Slist[idx]['arrival_time'] = now_time
        """
        here!!!!
        2020/4/26
        """
        sum_path_distance += path_distance
        # 获得两个partition的landmark的最短路径
    taxi_pos_node = ox.get_nearest_node(
        osm_map, (taxi_list[taxi_it].cur_lat, taxi_list[taxi_it].cur_lon))
    # print('the lon and lat of taxi_pos_node: {}, {}\n'.format(node_list[id_hash_map[taxi_pos_node]].lon, node_list[id_hash_map[taxi_pos_node]].lat))

    taxi_to_first_slist_node_path = nx.shortest_path(
        osm_map, source=taxi_pos_node, target=taxi_path.path_node_list[0].node_id, weight='length')
    taxi_to_first_slist_node_path = [Node(x, node_list[id_hash_map[x]].lon, node_list[id_hash_map[x]].lat,
                                          node_list[id_hash_map[x]].cluster_id_belongto) for x in taxi_to_first_slist_node_path]

    # if taxi_it == 0:
    #     print('check path')
    #     for kk in taxi_path.path_node_list:
    #         print(kk.node_id)

    taxi_path.path_node_list = taxi_to_first_slist_node_path + taxi_path.path_node_list

    # 加上了taxi目前位置到slist第一个节点的路径,因为上面的路径是不包括taxi原本位置的，只包括了slist里面的

    sum_path_distance += nx.shortest_path_length(
        osm_map, source=taxi_pos_node, target=taxi_path.path_node_list[0].node_id, weight='length')
    # 加上了taxi目前位置到slist第一个节点的路径长度,因为上面的路径是不包括taxi原本位置的，只包括了slist里面的

    path_cost = sum_path_distance / TYPICAL_SPEED
    return (taxi_path, path_cost)  # 一个Path对象和Path的cost


def possibility_routing(Slist, taxi_it):
    return 1, 2


def taxi_scheduling(candidate_taxi_list, req, req_id, mode=1):
    divide_group1()
    print('In taxi scheduling')
    print('正在处理的订单是： {}'.format(req_id))
    possible_insertion = []
    minimum_cost = 10 ** 10
    selected_taxi = -1
    selected_taxi_path = None
    res = []

    # for taxi_it in tqdm(candidate_taxi_list, 'scheduling'):
    for taxi_it in candidate_taxi_list:
        possible_insertion.clear()
        bnd = len(taxi_list[taxi_it].schedule_list)
        ori_cost = taxi_list[taxi_it].cur_total_cost
        if bnd == 1:
            # possible_insertion.append((1, 2))
            Slist = copy.deepcopy(taxi_list[taxi_it].schedule_list)
            start_point = {'request_id': req.request_id, 'schedule_type': 'DEPART', 'lon': req.start_lon,
                           'lat': req.start_lat, 'arrival_time': None}  # arrival_time在之后routing的时候确定
            end_point = {'request_id': req.request_id, 'schedule_type': 'ARRIVAL',
                         'lon': req.end_lon, 'lat': req.end_lat, 'arrival_time': None}
            Slist.insert(1, start_point)
            Slist.insert(2, end_point)
            if mode:
                new_path, cost = basic_routing(Slist, taxi_it)  # 写完basic routing就ok了
            else:
                new_path, cost = possibility_routing(Slist, taxi_it)
            if cost - ori_cost < minimum_cost:
                res = Slist
                minimum_cost = cost - ori_cost
                selected_taxi = taxi_it
                selected_taxi_path = new_path
        else:
            for i in range(1, bnd):
                for j in range(i + 1, bnd):
                    flag = insertion_feasibility_check(taxi_it, req, i, j)
                    if flag:
                        possible_insertion.append((i, j))

            for insertion in possible_insertion:
                Slist = copy.deepcopy(taxi_list[taxi_it].schedule_list)
                start_point = {'request_id': req.request_id, 'schedule_type': 'DEPART', 'lon': req.start_lon,
                               'lat': req.start_lat, 'arrival_time': None}  # arrival_time在之后routing的时候确定
                end_point = {'request_id': req.request_id, 'schedule_type': 'ARRIVAL',
                             'lon': req.end_lon, 'lat': req.end_lat, 'arrival_time': None}
                Slist.insert(insertion[0], start_point)
                Slist.insert(insertion[1] + 1, end_point)
                if mode:
                    new_path, cost = basic_routing(Slist, taxi_it)  # 写完basic routing就ok了
                else:
                    new_path, cost = possibility_routing(Slist, taxi_it)
                if cost - ori_cost < minimum_cost:
                    res = Slist
                    minimum_cost = cost - ori_cost
                    selected_taxi = taxi_it
                    selected_taxi_path = new_path

    if not selected_taxi_path:
        # taxi_list[selected_taxi].path.path_node_list = []   2020/4/21不知道这里用来干嘛的
        return selected_taxi, None

    global total_detour_cost
    total_detour_cost += minimum_cost

    taxi_list[selected_taxi].schedule_list = copy.deepcopy(res)
    taxi_list[selected_taxi].seat_left -= 1
    req_to_taxi_map[req_id] = selected_taxi
    if selected_taxi == 97:
        print('this is taxi 97')
        print('its schedule_list is')
        print(taxi_list[selected_taxi].schedule_list)
        print('res is')
        print(res)
    print('req_to_taxi_map[req_id] = {}'.format(req_to_taxi_map[req_id]))
    divide_group2()

    taxi_list[selected_taxi].path.path_node_list = selected_taxi_path.path_node_list
    return selected_taxi, selected_taxi_path.path_node_list


def empty_taxi_scheduling(candidate_taxi_list, req, req_id, mode=1):
    divide_group1()
    print('In empty_taxi_scheduling')
    print('正在处理的订单是： {}'.format(req_id))
    selected_taxi = -1
    min_distance = 10 ** 10
    order_start_point = ox.get_nearest_node(
        osm_map, (req.start_lat, req.start_lon))
    # for taxi_it in tqdm(candidate_taxi_list, 'scheduling'):
    for taxi_it in candidate_taxi_list:
        taxi_pos_node = ox.get_nearest_node(
            osm_map, (taxi_list[taxi_it].cur_lat, taxi_list[taxi_it].cur_lon))
        distance_taxi2order = node_distance_matrix[id_hash_map[order_start_point]
                                                   ][id_hash_map[taxi_pos_node]]
        if min_distance >= distance_taxi2order:
            min_distance = distance_taxi2order
            selected_taxi = taxi_it

    Slist = copy.deepcopy(taxi_list[selected_taxi].schedule_list)
    start_point = {'request_id': req.request_id, 'schedule_type': 'DEPART', 'lon': req.start_lon,
                   'lat': req.start_lat, 'arrival_time': None}  # arrival_time在之后routing的时候确定
    end_point = {'request_id': req.request_id, 'schedule_type': 'ARRIVAL',
                 'lon': req.end_lon, 'lat': req.end_lat, 'arrival_time': None}
    Slist.insert(1, start_point)
    Slist.insert(2, end_point)
    if mode:
        new_path, cost = basic_routing(Slist, taxi_it)  # 写完basic routing就ok了
    else:
        new_path, cost = possibility_routing(Slist, taxi_it)
    selected_taxi_path = new_path
    res = Slist
    taxi_list[selected_taxi].schedule_list = copy.deepcopy(res)
    if(selected_taxi == 97):
        print('97!!!!!!!!!!!!')
        print("97's schedule_list is")
        print(taxi_list[selected_taxi].schedule_list)
    taxi_list[selected_taxi].seat_left -= 1
    req_to_taxi_map[req_id] = selected_taxi
    print('req_to_taxi_map[req_id] = {}'.format(req_to_taxi_map[req_id]))
    divide_group2()
    taxi_list[selected_taxi].path.path_node_list = selected_taxi_path.path_node_list
    return selected_taxi, selected_taxi_path.path_node_list

# ==================================全局变量==============================================


conn = pymysql.connect(host='127.0.0.1', user='root',
                       passwd='', db='tenman', port=3308, charset='utf8')
cursor = conn.cursor(pymysql.cursors.SSCursor)

mobility_cluster = []
general_mobility_vector = []


TYPICAL_SPEED = 13.8889  # 单位是m/s
TAXI_TOTAL_NUM = 100
REQUESTS_TO_PROCESS = 500  # 总共要处理多少个request
partition_filter_param = 1.0

Lambda = 0.5
# alpha = 0.999999921837146
node_list = []  # Node对象
taxi_list = []  # Taxi对象
taxi_status_queue = []  # taxi的事件队列
request_list = {}
partition_list = []
landmark_list = []
print('再等等，好了我会告诉你')
files = glob.glob('mTshare/data/node_distance/node_distance_*.csv')
node_distance = pd.read_csv(files[0])
node_distance = node_distance.loc[:, ~
                                  node_distance.columns.str.contains('^Unnamed')]
for idx in range(1, len(files)):
    tmp = pd.read_csv(files[idx])
    tmp = tmp.drop(['Unnamed: 0'], axis=1)
    node_distance = node_distance.append(tmp)

node_distance_matrix = []
now_time = 0
socket = None

total_detour_cost = 0
# ==================================全局变量==============================================


def send_info(msg):
    socket.send(text_data=json.dumps(msg))


def main(socket1):
    global socket
    global now_time
    socket = socket1
    req_cnt = 0
    system_init()
    order_index = 0
    last_time = SYSTEM_INIT_TIME - TIME_OFFSET  # 初始化为开始时间
    f = open('mTshare/data/testresult.txt', 'w')
    while True:
        if req_cnt > REQUESTS_TO_PROCESS:
            break
        now_time = time.time() - TIME_OFFSET
        reqs = request_fetcher(last_time, now_time)
        last_time = now_time
        if len(reqs) == 0:
            continue
        else:
            # for req_item in tqdm(reqs, desc='Processing requests...'):
            for req_item in reqs:
                color = random_color()
                print(
                    '**********************************************************************')
                print(
                    '**************************新订单{}**************************************'.format(req_cnt))
                print(
                    '**********************************************************************')
                end_time = req_item[1] + datetime.timedelta(minutes=15).seconds
                """
                0: order_id,
                1: start_time,
                2: end_time,
                3: start_longitude,
                4: start_latitude,
                5: end_longitude,
                6: end_latitude
                """
                start_node_id = ox.get_nearest_node(
                    osm_map, (req_item[4], req_item[3]))
                socket_request = {'type': 'request_pos', 'content': {'value': wgs84_to_bd09(req_item[3], req_item[4]), 'itemStyle': {'color': 'white'}},
                                  'content1': {'value': wgs84_to_bd09(req_item[5], req_item[6]), 'itemStyle': {'color': 'white'}}, 'time': time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(now_time))}
                send_info(socket_request)
                end_node_id = ox.get_nearest_node(
                    osm_map, (req_item[6], req_item[5]))
                time_on_tour = node_distance_matrix[id_hash_map[start_node_id]
                                                    ][id_hash_map[end_node_id]]

                req_item = Request(req_cnt, req_item[3], req_item[4], req_item[5],
                                   req_item[6], start_node_id, end_node_id, req_item[1], req_item[2])
                divide_group1()
                print('订单消息：')
                print('起点经纬度：{} ,终点经纬度：{} '.format(wgs84_to_bd09(req_item.start_lon,
                                                                 req_item.start_lat), wgs84_to_bd09(req_item.end_lon, req_item.end_lat)))
                divide_group2()

                req_item.config_pickup_deadline(req_item.delivery_deadline - time_on_tour)
                request_list[req_cnt] = req_item
                req_cnt += 1
                print('release time is {}'.format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(req_item.release_time))))
                # 用当前moment来更新所有taxi, mobility_cluster和general_cluster
                update(req_item)
                candidate_taxi_list, candidate_empty_list, candidate_non_empty_list = taxi_req_matching(req_item)
                divide_group1()
                print('mv符合的非空车: ')
                print(candidate_taxi_list)
                print('mv 不 符合的空车: ')
                print(candidate_empty_list)
                print('mv 不 符合的非空车: ')
                print(candidate_non_empty_list)
                # 发送的士的位置
                socket_taxi_list = [wgs84_to_bd09(i.cur_lon, i.cur_lat) for i in taxi_list]
                socket_taxi_list = {'type': 'all_taxi', 'content': socket_taxi_list}
                send_info(socket_taxi_list)
                divide_group2()
                # 如果没有候选taxi会返回none
                cost = None
                if candidate_taxi_list == None and candidate_empty_list == None and candidate_non_empty_list == None:
                    print('这个订单没有taxi')
                    print('该订单结束//////////////////////////////////////')
                    input('天啊！居然出现了没有人回应的订单！！！点击回车继续')
                    continue
                    divide_group2()
                elif len(candidate_taxi_list) != 0:
                    chosen_taxi, cost = taxi_scheduling(candidate_taxi_list, req_item, req_item.request_id, 1)
                if cost == None and len(candidate_empty_list) != 0:
                    chosen_taxi, cost = empty_taxi_scheduling(candidate_empty_list, req_item, req_item.request_id, 1)
                if cost == None and len(candidate_non_empty_list) != 0:
                    chosen_taxi, cost = taxi_scheduling(candidate_non_empty_list, req_item, req_item.request_id, 1)
                show_taxi = taxi_list[chosen_taxi]
                req_item.color = show_taxi.color
                non_empty_taxi_set.add(show_taxi)
                print('这个订单选中的taxi是{}'.format(chosen_taxi))

                socket_chosen_taxi = {'type': 'chosen_taxi', 'content': {'coords': [
                    wgs84_to_bd09(node.lon, node.lat) for node in show_taxi.path.path_node_list]}}
                send_info(socket_chosen_taxi)
                # socket_order_details =

                socket_all_request_start = {'type': 'all_request_start', 'content':
                                            [{'value': wgs84_to_bd09(item.start_lon, item.start_lat), 'itemStyle': {'color': item.color}, 'name': "起点_{}".format(item.request_id)} for item in request_list.values()]}
                send_info(socket_all_request_start)
                socket_all_request_end = {'type': 'all_request_end', 'content':
                                          [{'value': wgs84_to_bd09(item.end_lon, item.end_lat), 'itemStyle': {'color': item.color}, 'name': "终点_{}".format(item.request_id)} for item in request_list.values()]}
                send_info(socket_all_request_end)
                socket_all_non_empty_taxi = {'type': 'all_non_empty_taxi', 'content':
                                             [{'value': wgs84_to_bd09(item.cur_lon, item.cur_lat), 'itemStyle': {'color': item.color}, 'name': "的士_{}".format(item.taxi_id)} for item in non_empty_taxi_set]}
                send_info(socket_all_non_empty_taxi)
                print('的士的位置：')
                for item in non_empty_taxi_set:
                    print('taxi_{}:{} {}'.format(item.taxi_id, item.cur_lon, item.cur_lat))

                socket_taxi_path = {'type': 'taxi_path',
                                    'content': [{
                                                'coords': [wgs84_to_bd09(node.lon, node.lat) for node in item.path.path_node_list], 
                                                'lineStyle':{'color': item.color},
                                                'name': "的士_{}".format(item.taxi_id),
                                                'ok': '0%'
                                                }
                                                for item in non_empty_taxi_set]}
                send_info(socket_taxi_path)
                socket_taxi_path_start = {'type': 'taxi_path_start',
                                          'content': [{'value': wgs84_to_bd09(item.path.path_node_list[0].lon, item.path.path_node_list[0].lat), 'itemStyle':{'color': item.color}, 'name': "taxi_{}起点".format(item.taxi_id)}
                                                      for item in non_empty_taxi_set]}
                send_info(socket_taxi_path_start)
                show_taxi.show_schedule()
                show_taxi.show_pos()
                # 发送最新状态

                print('该订单结束//////////////////////////////////////')
                global total_detour_cost
                f.write('total served requests: %d\n' % req_cnt)
                f.write('total detour time: %f\n' % total_detour_cost)
                divide_group2()


print('载入完毕')

# main()

# cursor.close()
# conn.close()
