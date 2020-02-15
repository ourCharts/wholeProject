"""ourcharts URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url
import taxi.views as taxi_view
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
urlpatterns = [
    url(r'^test/$', taxi_view.test),
    url(r'^initial_status/$', taxi_view.initial_status),
    url(r'^track_onetime/$', taxi_view.track_onetime),
    path('chat/', include('chat.urls')),
    path('room/', taxi_view.track),
    url(r'^$', TemplateView.as_view(template_name="index.html")),
    url(r'^all_id/$', taxi_view.get_allId),
]
