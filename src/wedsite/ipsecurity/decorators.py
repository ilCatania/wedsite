try:
    from functools import update_wrapper
except ImportError:
    from django.utils.functional import update_wrapper  # Python 2.3, 2.4 fallback.
from django import http
import datetime
import models

MAX_DAILY_ACTIONS = 20

def limit_daily_actions(function=None):
    def decorate(view_func):
        return _CheckIpActivity(view_func)
    if(function):
        return decorate(function)
    return decorate

class _CheckIpActivity(object):
    def __init__(self, view_func):
        self.view_func = view_func
        update_wrapper(self, view_func)
        
    def __get__(self, obj, cls=None):
        view_func = self.view_func.__get__(obj, cls)
        return _CheckIpActivity(view_func)
    
    def __call__(self, request, *args, **kwargs):
        err = False
        if(request.method == 'POST'):
            if 'REMOTE_ADDR' in request.META and request.META['REMOTE_ADDR']:
                ip_addr = request.META['REMOTE_ADDR']
                if not self.check_actions_today(ip_addr):
                    err = 'Your IP: %s was suspended due to excessive activity.' % ip_addr + \
                        'Please try again tomorrow, or contact the webmaster.'
                    #todo: send an e-mail here?
            else:
                err = 'Invalid ip address, action disabled.'
        if err:
            return http.HttpResponseForbidden(err)
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
        