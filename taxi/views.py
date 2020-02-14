import json

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
        res = "nothin got!"
    print(type(res),"     ",res)
    #val = serialize("json",res)
    #print(val)
    return JsonResponse(list(res),safe=False)

def test(request):
    return render(request,"showuser.html")

def track(request):
    return render(request,"room.html")