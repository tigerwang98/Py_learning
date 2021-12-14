from django.shortcuts import render
from django.db import connection

def get_cursor():
    return connection.cursor()

def index(request):
    cursor = get_cursor()
    cursor.execute('select id,book_name,author from `django_data`')
    data = cursor.fetchall()
    books = {"data": data}
    return render(request, 'index.html', context=books)

def add_book(request):
    return render(request, 'add_book.html')

def handle_book(request):
    pass