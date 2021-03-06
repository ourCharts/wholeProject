from mTshare.MobilityVector import MobilityVector
from mTshare.Tool.Tool import *
from mTshare.Path import Path
import time
print('载入Taxi中')

king_make_order_finished = set()

class Taxi:
    cur_total_cost = 0

    def __init__(self, taxi_id, cur_lon, cur_lat, init_last_update_time, partition_id_belongto, seat_left, mobility_vector=None):
        self.seat_left = (3 if seat_left == None else seat_left)
        self.taxi_id = taxi_id
        self.cur_lon = cur_lon
        self.cur_lat = cur_lat
        self.schedule_list = [{'request_id': -1, 'schedule_type': 'NO_ORDER',
                               'lon': cur_lon, 'lat': cur_lat, 'arrival_time': init_last_update_time}]
        # schedule list中保存的是字典, 里面的内容包括: request_id: request_id, schedule_type: shedule的类型(出发或到达), lon: 经度, lat: 纬度, arrival_time: 计算出来的预期到达时间
        self.__last_update_time = init_last_update_time
        self.partition_id_belongto = partition_id_belongto
        self.mobility_vector = mobility_vector
        self.path = Path(init_last_update_time)  
        self.cur_total_cost = 0
        self.seat_left = seat_left
        self.capability = self.seat_left
        self.color = random_color()
        self.complete_index = 0
        self.__guest = None
    
    def __guest_clear(self):
        for i in self.__guest:
           king_make_order_finished.add(i)
        self.__guest = None

    def get_guest(self):
        return self.__guest


    def add_guest(self, order_id:int):
        if self.__guest == None:
            self.__guest = set([order_id])
        else:
            self.__guest.add(order_id)
        return

    def show_schedule(self):
        print('showing schedule: This is taxi {}'.format(self.taxi_id))
        for idx, node in enumerate(self.schedule_list):
            print('{}. {},经纬度：{},{}, 到达时间：{}, 时间戳: {}'.format(idx,node['schedule_type'],node['lon'],node['lat'],time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(node['arrival_time'])), node['arrival_time']))

    def show_pos(self):
        print('Taxi {}的位置是：{}   {}'.format(self.taxi_id,self.cur_lon,self.cur_lat))


    def show_path_list(self):
        print('showing schedule: This is taxi {}'.format(self.taxi_id))
        self.path.get_node_list()


    def is_available(self):
        if self.seat_left > 0:
            return True
        return False

    def is_empty(self):
        if self.seat_left == self.capability:
            return True
        return False

    def update_schedule(self, moment):
        
        print('in update_schedule, this is taxi {}'.format(self.taxi_id))
        if len(self.schedule_list) == 1 and self.schedule_list[0]['request_id'] == -1:
            return
        print('taxi {} 正在更新状态：'.format(self.taxi_id))
        # self.show_path_list()
        del_list =[]
        for idx, schedule_node in enumerate(self.schedule_list):
            if schedule_node['arrival_time'] < moment:
                del_list.append(idx)
        for i in range(len(del_list)-1, -1, -1):
            if self.schedule_list[del_list[i]]['schedule_type'] == 'ARRIVAL':
                self.seat_left += 1
            del self.schedule_list[del_list[i]]
        print('这个是del_list {}'.format(del_list))
        print('更新前的schedule_list')
        self.show_schedule()
        print("更新后的schedule_list")
        self.show_schedule()

    def update_status(self, moment):
        if self.schedule_list[0]['schedule_type'] == 'NO_ORDER' and len(self.schedule_list) == 1:
            return 
        # 状态： cur_lon、cur_lon、__last_update_time
        #		 schedule_list 、partition_id_belongto、mobility_vector
        self.__last_update_time = moment
        
        self.update_schedule(moment)

        # 更新经纬度
        if len(self.path.path_node_list) == 0:
            return
        print()
        print('$ taxi id is {}'.format(self.taxi_id))
        print('before updating, the position is lon: {}, lat: {}'.format(self.cur_lon, self.cur_lat))
        tmp_result = self.path.get_position(moment)
        print("schedule_node_list长度：{}".format(len(self.schedule_list)))
        if len(tmp_result) == 3 and len(self.schedule_list) != 0:
            self.cur_lon, self.cur_lat,self.complete_index = tmp_result
            self.partition_id_belongto = check_in_which_partition(
            self.cur_lon, self.cur_lat)
        elif len(tmp_result)==2  or len(self.schedule_list) == 0:
            self.__guest_clear()
            if len(tmp_result) == 3:
                self.cur_lon, self.cur_lat,self.complete_index = tmp_result

            self.partition_id_belongto = check_in_which_partition(
            self.cur_lon, self.cur_lat)
        # print('after updating, the position is lon: {}, lat: {}'.format(self.cur_lon, self.cur_lat))
        # if self.path.is_over(moment) == -1 or len(self.schedule_list) == 0:
            # if self.path.is_over(moment) == -1:
            #     print("self.path.is_over(moment)")
            # else:
            #     print("len(self.schedule_list) == 0")
            self.path = Path(moment)
            self.schedule_list = [{'request_id': -1, 'schedule_type': 'NO_ORDER',
                                   'lon': self.cur_lon, 'lat': self.cur_lat, 'arrival_time': self.__last_update_time}]
            self.mobility_vector = None
            self.complete_index = 0
            non_empty_taxi_set.remove(self)
            print('taxi_{}update over(path over)'.format(self.taxi_id))
            return

        # mobility-vector的更新
        average_lon = average_lat = 0
        sum_item = 0
        for sch_node in self.schedule_list:
            if sch_node['schedule_type'] != 'ARRIVAL':
                continue
            average_lat += sch_node['lon']
            average_lon += sch_node['lat']
            sum_item += 1
        print('in taxi\'s update_status, len(self.schedule_list) is {}, self.schedule_list is {}, sum_item is {}'.format(len(self.schedule_list), self.schedule_list, sum_item))
        average_lat /= sum_item
        average_lon /= sum_item
        self.mobility_vector = MobilityVector(
            self.cur_lon, self.cur_lat, average_lon, average_lat, "TAXI", self.taxi_id)
        print('taxi_{} update over'.format(self.taxi_id))
