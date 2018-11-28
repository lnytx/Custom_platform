# -*- coding: utf-8 -*-  
'''
Created on 2018年1月4日

@author: ning.lin
'''
from django.conf import settings


EXEMPT_URLS=[compile(settings.LOGIN_URL.lstrip('/'))]
print("EXEMPT_URLS",EXEMPT_URLS)