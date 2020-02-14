from channels.generic.websocket import WebsocketConsumer
import json
from chat import models
import time
from django.http import request


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()

    def disconnect(self, close_code):
        pass

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        print(message)
        msg = message
        try:
            res = models.Position.objects.filter(order_id=msg)  # eb9dd4095d9850e6287cefd813775a6c
        except:
            res = ""
        val = {}

        print(type(res))
        for i in res:
            message = {}
            message['time_stamp'] = i.time_stamp
            message['order_id'] = i.order_id
            message['driver_id'] = i.driver_id
            message['longitude'] = i.longitude
            message['latitude'] = i.latitude
            print(message)
            self.send(text_data=json.dumps({
                'message': message
            }))
            time.sleep(0.1)#设置发送间隔时间单位（秒）
        self.disconnect()
