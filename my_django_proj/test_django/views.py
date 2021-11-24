from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect, reverse

# Create your views here.
def test_param(request, pid):
    return HttpResponse('获取到了链接中参数是pid:%s' % pid)

def test_kw(request):
    kw = request.GET.get('kw')
    return HttpResponse('获取到了链接中的查询字符串为：%s' % kw)

def echo_index(request):
    username = request.GET.get('username')
    if username:
        return HttpResponse('这是首页！')
    else:
        return redirect(reverse('test_django:denglu'))

def echo_login(request):
    return HttpResponse('这是登录页面！')