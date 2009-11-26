import os, sys
sys.path.append("/home/gcatania/public_html");
sys.path.append("/home/gcatania/public_html/wedsite");
os.environ['DJANGO_SETTINGS_MODULE'] = 'wedsite.settings'
os.environ['PYTHON_EGG_CACHE'] = '/home/gcatania/.python_egg_cache'
import django.core.handlers.wsgi
_application = django.core.handlers.wsgi.WSGIHandler()
def application(environ, start_response):
    #don't set it, and don't ask
    #environ['PATH_INFO'] = environ['SCRIPT_NAME'] + environ['PATH_INFO']
    return _application(environ, start_response)
