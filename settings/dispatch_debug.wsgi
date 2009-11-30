import os, sys
sys.path.append("/home/gcatania/public_html");
sys.path.append("/home/gcatania/public_html/wedsite");
os.environ['DJANGO_SETTINGS_MODULE'] = 'wedsite.settings'
os.environ['PYTHON_EGG_CACHE'] = '/home/gcatania/.python_egg_cache'
import django.core.handlers.wsgi
#_application = django.core.handlers.wsgi.WSGIHandler()




from threading import Lock
from pprint import pformat
try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO

from django import http
from django.core import signals
from django.core.handlers import base
from django.core.urlresolvers import set_script_prefix
from django.utils import datastructures
from django.utils.encoding import force_unicode

import traceback

class WSGIHandler(base.BaseHandler):
    initLock = Lock()
    request_class = django.core.handlers.wsgi.WSGIRequest

    def __call__(self, environ, start_response):
        from django.conf import settings

        # Set up middleware if needed. We couldn't do this earlier, because
        # settings weren't available.
        if self._request_middleware is None:
            self.initLock.acquire()
            # Check that middleware is still uninitialised.
            if self._request_middleware is None:
                self.load_middleware()
            self.initLock.release()

        set_script_prefix(base.get_script_name(environ))
        signals.request_started.send(sender=self.__class__)
        try:
            try:
                request = self.request_class(environ)
            except UnicodeDecodeError:
                response = http.HttpResponseBadRequest()
            else:
                response = self.get_response(request)

                # Apply response middleware
                for middleware_method in self._response_middleware:
                    response = middleware_method(request, response)
                response = self.apply_response_fixes(request, response)
        finally:
            signals.request_finished.send(sender=self.__class__)

        try:
            status_text = django.core.handlers.wsgi.STATUS_CODE_TEXT[response.status_code]
        except KeyError:
            status_text = 'UNKNOWN STATUS CODE'
        status = '%s %s' % (response.status_code, status_text)
        response_headers = [(str(k), str(v)) for k, v in response.items()]
        for c in response.cookies.values():
            response_headers.append(('Set-Cookie', str(c.output(header=''))))
        #start_response(status, response_headers)
        #return response
        d = []
        try:
            return str(response)
        except:
            type, value, tb = sys.exc_info()
            #test = str([sys.stderr,  type.__name__, ":", value.message, sys.stderr, '\n'.join(traceback.format_tb(tb))])
            test = str([type.__name__, ":", value.message, '\n'.join(traceback.format_tb(tb))])



def application(environ, start_response):
    #dunno why it's not populated, set it manually
    #environ['PATH_INFO'] = u'/dispatch.wsgi' + environ['PATH_INFO']
    #environ['PATH_INFO'] = environ['SCRIPT_NAME'] + environ['PATH_INFO']
    try:
            _application = WSGIHandler()
            test = _application(environ, start_response)
    except:
        type, value, tb = sys.exc_info()
        #test = sys.stderr #str([sys.stderr,  type.__name__, ":", value.message, sys.stderr, '\n'.join(traceback.format_tb(tb))])
        test = str(value) #str([type.__name__, ":", value.message]) #,'\n'.join(traceback.format_tb(tb))])
    else:
        test = 'stica'
    status = '200 OK' 
    response_headers = [('Content-type', 'text/plain'),
                        ('Content-Length', str(100+len(test)))]
    start_response(status, response_headers)
    return [test]