# encoding: utf-8
"""
@project = Py_learing
@file = urls
@author= wanghu
@create_time = 2021/11/30 15:07
"""
from django.urls import path
from book_manager import views

# app_name = 'book_manager'

urlpatterns = [
    path('index', views.index, name='index'),
    path('add_book', views.add_book, name='add_book'),
    path('book_detail', views.handle_book, name='book_detail'),
]