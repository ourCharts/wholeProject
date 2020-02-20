import json
import random

from django.core.serializers import serialize
from django.core.serializers.json import DjangoJSONEncoder
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from . import models
# Create your views here.

def initial_status(request):
    msg = request.GET.get("order_id", False)
    try:
        res = models.Myorder.objects.get(order_id=msg)  # eb9dd4095d9850e6287cefd813775a6c
    except:
        res = ""
    val = {}
    if res!="":
        val['order_id'] = res.order_id
        val['start_time'] = res.start_time
        val['end_time'] = res.end_time
        val['start_longitude'] = res.start_longitude
        val['start_latitude'] = res.start_latitude
        val['end_longitude'] = res.end_longitude
        val['end_latitude'] = res.end_latitude
    print(val)
    return JsonResponse(val)

def track_onetime(request):
    msg = request.GET.get("order_id", False)
    try:
        res = models.Position.objects.filter(order_id=msg).values()  # eb9dd4095d9850e6287cefd813775a6c
    except:
        res = "nothing got!"
    print(type(res),"     ",res)
    #val = serialize("json",res)
    #print(val)
    return JsonResponse(list(res),safe=False)

def get_allId(request):
    try:
        res = models.Myorder.objects.values('order_id')  # eb9dd4095d9850e6287cefd813775a6c
    except:
        res = "nothing got!"
    print(res)
    return JsonResponse(list(res),safe=False)

def test(request):
    return render(request,"showuser.html")

def track(request):
    return render(request,"room.html")

def random_track(request):
    num = int(request.GET.get("track_num", False))
    try:
        res = models.Myorder.objects.values('order_id')
    except:
        res = ""
    random.seed()
    order_id = random.sample(list(res),num)
    print(order_id)
    # print(order_id[1]['order_id'])
    arr = []
    try:
        for id in order_id:
            print(id['order_id'])
            temp = order(id['order_id'])
            res = models.Position.objects.filter(order_id=id['order_id']).values()
            #print(res)
            coor = [[i['longitude'],i['latitude']]  for i in res]
            #print(coor)
            temp.__add__(coor)
            arr.append(temp.__str__())
    except:
        res = "nothing got!"
        print("error error error error error error error error error error error error error error error")
    #print(arr[0])

    return JsonResponse(arr,safe=False)

class order:
    order_id  = ""
    coords = []
    lineStyle = {}
    def __init__(self,o):
        self.order_id = o
        r = format(round((105+150*random.random())),'x')
        g = format(round((105+150*random.random())),'x')
        b = format(round((105+150*random.random())),'x')
        self.lineStyle['color'] = '#'+r+g+b
    def __add__(self, other):
        self.coords = other

    def __str__(self):
        val = {}
        val['order_id']=self.order_id
        val['coords']=self.coords
        val['lineStyle']=self.lineStyle
        print(val)
        return val



