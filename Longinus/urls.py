# -*- coding: UTF-8 -*-

from django.conf.urls import url, include
from django.conf import settings
from django.conf.urls.static import static

from . import views, views_ajax

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^redisScan/$', views.redisScan, name='redisScan'),
    url(r'^getRedisList/$', views_ajax.getRedisList, name='getRedisList'),
    url(r'^execCommand/$', views_ajax.execCommand, name='execCommand'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
