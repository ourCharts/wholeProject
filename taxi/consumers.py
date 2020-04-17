from channels.generic.websocket import WebsocketConsumer
import json
import time
from django.http import request
from mTshare.main import *

class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()
        print('连接上客户端!')
        main(self)

    def disconnect(self, close_code):
        print("bye bye", close_code)
        pass

    def receive(self, text_data):
        # print(text_data)
        # 对前端的心跳包作出回应
        if text_data=="ping":
            self.send(text_data=json.dumps({
                  'message': "pong"
            }))
            # print("pong")

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
