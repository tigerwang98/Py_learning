# encoding: utf-8
"""
@project = Py_learing
@file = urls
@author= wanghu
@create_time = 2021/11/24 14:35
"""
from django.urls import path
from test_django import views

# 链接反转时需要指定命令空间
app_name = 'test_django'

urlpatterns = [
    path('index', views.echo_index, name='shouye'),
    path('login', views.echo_login, name='denglu'),
    path('param/<int:pid>', views.test_param, name='param'),
    path('kw', views.test_kw, name='kw'),
    path('render', views.echo_render, name='render'),
    path('render/p/1', views.echo_com_render, name='render_1')
]