from channels.generic.websocket import WebsocketConsumer
import json
import time
from django.http import request
from mTshare.main import *
import threading
from multiprocessing import Process
from multiprocessing import Pool
from copy import deepcopy

def defMain():
    _self = nothing.pop
    main(_self)

nothing = []

class ChatConsumer(WebsocketConsumer):
    __process = Process()
    pool = Pool()
    firstIn = False
    # def __init__(self, scope):
    #     self.scope = scope

    def connect(self):
        self.accept()
        print('连接上客户端!')
        # os.system(main(self))
        if ChatConsumer.firstIn==True:
            ChatConsumer.pool.close()
        #     ChatConsumer.__process.terminate()
        #     ChatConsumer.__process.close()
        ChatConsumer.firstIn = True
        nothing.append(self)
        # ChatConsumer.__process = Process(target=main, args=((self,)))
        # ChatConsumer.__process.start()      
        ChatConsumer.pool.apply_async(func=defMain)
        print('{} start'.format(os.getpid()))

    def disconnect(self, close_code):
        print("bye bye!", close_code)
        pass

    def receive(self, text_data):
        # print(text_data)
        # 对前端的心跳包作出回应
        if text_data=="ping":
            self.send(text_data=json.dumps({
                  'message': "pong"
            }))
            # print("pong")

    def ExecuteMain(self):
        _self = nothing.pop()
        main(_self)

    # def receive(self, text_data):
    #     text_data_json = json.loads(text_data)
    #     message = text_data_json['message'] # 接收前台查询条件
    #     print(message)
    #     msg = message
    #     try:
    #         res = models.Position.objects.filter(order_id=msg)  # eb9dd4095d9850e6287cefd813775a6c
    #     except:
    #         res = ""
    #     val = {}

    #     print(type(res))
    #     for i in res:
    #         message = {}
    #         message['time_stamp'] = i.time_stamp
    #         message['order_id'] = i.order_id
    #         message['driver_id'] = i.driver_id
    #         message['longitude'] = i.longitude
    #         message['latitude'] = i.latitude
    #         print(message)
    #         self.send(text_data=json.dumps({
    #             'message': message
    #         }))
    #         time.sleep(0.1)###  设置发送间隔时间单位（秒）

        #传输完毕自动关闭连接
        # self.disconnect()
