from django.core import serializers
from django.shortcuts import render, redirect, HttpResponse
from django.views.generic.base import View
from rest_framework.views import APIView, Response


# Create your views here.
class BookDetail(View):
    def get(self,request,pk):
        return HttpResponse("get ..."+ pk)   # 查看某本书籍

    def put(self,request,pk):
        return HttpResponse("put ..." + pk)  # 查看某本书籍

    def post(self,request,pk):
        return HttpResponse("post ..." + pk) # 添加某本书籍

    def delete(self,request,pk):
        return HttpResponse("delete ..." + pk) # 删除某本书籍
    
class PublishView(APIView):
    def get(self,request):
        # 取数据 APIView
        msg=[1,2,3,4,'a','b',]
        # [OrderedDict([('name', '苹果出版社'), ('email', '123@qq.com')]),
        # OrderedDict([('name', '橘子出版社'), ('email', '456@qq.com')])]
        from rest_framework.request import Request
        print(request.GET)  # <QueryDict: {'a': ['1'], 'b': ['2']}>
        print("data",request.data) #  # 只处理 post
        print(request._request.GET) # <QueryDict: {'a': ['1'], 'b': ['2']}>
        return HttpResponse(msg)
        # return Response(ret.data)

    def post(self,request):
        # 取数据  View              （原生request支持得操作）
        # print("post",request.POST) # <QueryDict: {'a': ['1'], 'b': ['2']}>
        # print("body",request.body) #  b'a=1&b=2'

        # 发的是json数据  View (不处理json数据，只解析urlencode)   （原生request支持得操作）
        # print("post", request.POST)  # <QueryDict: {}>
        # print("body", request.body)  # b'{"name":"yuan","age":12}'

        # print(type(request)) # <class 'django.core.handlers.wsgi.WSGIRequest'>
        # from django.core.handlers.wsgi import WSGIRequest

        # APIView    （新得request支持得操作）
        print(type(request)) # <class 'rest_framework.request.Request'>
        from rest_framework.request import Request
        print(request._request) # <WSGIRequest: POST '/publishes/'>
        print("data",request.data)  # {'name': 'yuan', 'age': 12}
        print("type",type(request.data)) #  <class 'dict'>
        return HttpResponse('POST')
