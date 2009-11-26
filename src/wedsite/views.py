'''
Created on 03/ott/2009

@author: Gabriele
'''
from django.conf import settings
from django.shortcuts import render_to_response
from django.template import RequestContext
from django import http
from django.views import defaults as viewdefaults
from news.models import News 
from polls.models import Poll
import random
from django.contrib.auth import authenticate, login

def start(request):
    if ((hasattr(request, 'session') and 'django_language' in request.session) 
        or settings.LANGUAGE_COOKIE_NAME in request.COOKIES):
        return http.HttpResponseRedirect("/home/")
    else:
        return http.HttpResponseRedirect("/lang/")

def do_login(request):
    if(request.method == 'POST'):
        username = request.POST['u']
        password = request.POST['p']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
            return http.HttpResponseRedirect("/")
    return http.HttpResponseRedirect("/login/")

def home(request):
    return render_to_response('home/home.djhtml', 
                              {'content_class':'home',
                               'news_items': News.objects.all()[:2],
                               'polls': Poll.objects.all()[:3] },
                               context_instance=RequestContext(request))

def wip(request):
    return render_to_response('wip.djhtml',
                              {'img_no': random.choice([1, 2])},
                              context_instance=RequestContext(request))

#error code 404
def page_not_found(request):
    return viewdefaults.page_not_found(request, '404.djhtml')

#error code 500
def server_error(request):
    return viewdefaults.server_error(request, '500.djhtml')
