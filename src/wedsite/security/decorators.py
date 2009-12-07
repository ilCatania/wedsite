try:
    from functools import update_wrapper
except ImportError:
    from django.utils.functional import update_wrapper  # Python 2.3, 2.4 fallback.
from django import http
import utils
import datetime
import models

MAX_DAILY_ACTIONS = 20
AUTHORIZATION_COOKIE_NAME = 'authorized'

#
# not yet implemented fully
#
def passwprd_protect(function=None):
    def decorate(view_func):
        return _CheckIpActivity(view_func)
    if(function):
        return decorate(function)
    return decorate

def limit_daily_actions(function=None):
    def decorate(view_func):
        return _CheckIpActivity(view_func)
    if(function):
        return decorate(function)
    return decorate

#
# not yet implemented fully
#
class _PasswordProtect(object):
    def __init__(self, view_func):
        self.view_func = view_func
        update_wrapper(self, view_func)
    def __get__(self, obj, cls=None):
        view_func = self.view_func.__get__(obj, cls)
        return _PasswordProtect(view_func)
    
    def __call__(self, request, *args, **kwargs):
        if(request.method == 'POST'):
            if 'REMOTE_ADDS' in request.META and request.META['REMOTE_ADDR']:
                ip_addr = request.META['REMOTE_ADDR']
                if self.check_cookie_content(request, ip_addr):
                    return self.view_func(request, *args, **kwargs)
                if self.check_password(request):
                    response = self.view_func(request, *args, **kwargs)
                    response.set_cookie(AUTHORIZATION_COOKIE_NAME, 
                        utils.encrypt(ip_addr),
                        max_age=60 * 60 * 24 * 60) #two months
                    return response                  
            else:
                return http.HttpResponseForbidden('Invalid ip address, action disabled.')
        #todos
        return None #should return password prompt - todo
            
    def check_cookie_content(self, ip_addr, cookie):
        pass #todo
    def check_password(self, request):
        pass #todo

class _CheckIpActivity(object):
    def __init__(self, view_func):
        self.view_func = view_func
        update_wrapper(self, view_func)
        
    def __get__(self, obj, cls=None):
        view_func = self.view_func.__get__(obj, cls)
        return _CheckIpActivity(view_func)
    
    def __call__(self, request, *args, **kwargs):
        if(request.method == 'POST'):
            if 'REMOTE_ADDR' in request.META and request.META['REMOTE_ADDR']:
                ip_addr = request.META['REMOTE_ADDR']
                if not self.check_actions_today(ip_addr):
                    return http.HttpResponseForbidden('Your IP: %s was suspended due to excessive activity.' % ip_addr + \
                        'Please try again tomorrow, or contact the webmaster.')
                    #todo: send an e-mail here?
            else:
                return http.HttpResponseForbidden('Invalid ip address, action disabled.')
        return self.view_func(request, *args, **kwargs)
            
    def check_actions_today(self, ip_addr):
        qs=models.LoggedAction.objects.filter(ip_addr=ip_addr)
        #if qs.exists(): #not sure if version up to date
        if bool(qs):
            la = qs[0]
            if la.banned:
                return False
            if la.last_action.date() >= datetime.date.today():
                if la.action_count >= MAX_DAILY_ACTIONS:
                    return False
            else:
                #no actions today
                la.action_count = 0
        else:
            la=models.LoggedAction(ip_addr=ip_addr)
        la.action_count = la.action_count + 1
        la.save()
        return True
        