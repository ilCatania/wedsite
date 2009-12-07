from django.conf.urls.defaults import patterns, include
from django.contrib import admin
import views
import settings

admin.autodiscover()

handler404 = 'wedsite.views.page_not_found'
handler500 = 'wedsite.views.server_error'

urlpatterns = patterns('',
    (r'^$', views.start),
    (r'^home/$', views.home),
    (r'^wedding/$', 'activities.views.todo_list', {'template': 'wedding/wedding.djhtml',
                                                   'slug': 'wedding'}),
    (r'login/do/$', views.do_login),
    (r'^wip/$', views.wip),
    (r'^jslang/$', 'django.views.i18n.javascript_catalog', { 'packages': ('wedsite',), }),
    (r'^404.shtml$', handler404),
    (r'^500.shtml$', handler500),
    (r'^admin/(.*)', admin.site.root),
    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),
)
if(settings.DEV_MACHINE):
    # development only
    docroot = 'C:/workspaces/django/wedsite/wedsite_static'
    urlpatterns += patterns('django.views.static',
        (r'^layout/(?P<path>.*)$', 'serve', {'document_root': docroot + '/layout'}),
        (r'^js/(?P<path>.*)$', 'serve', {'document_root': docroot + '/js'}),
        (r'^img/(?P<path>.*)$', 'serve', {'document_root': docroot + '/img'}),
    )
    
urlpatterns += patterns('django.views.generic.simple',
    (r'^login/$', 'direct_to_template', {'template': 'login.djhtml'}),
    (r'^lang/$', 'direct_to_template', {'template': 'i18n/setlang.djhtml', 
                                        'extra_context': {'body_class': 'lang'}}),
    (r'^wedding/gifts/$', 'direct_to_template', {'template': 'wedding/gifts.djhtml'}),
    (r'^home/about/$', 'redirect_to', {'url': '/wip/', 'permanent': False}),
    (r'^home/contact/$', 'redirect_to', {'url': '/wip/', 'permanent': False}),
    (r'^us/$', 'redirect_to', {'url': '/wip/', 'permanent': False}),
    (r'^us/betrothed/$', 'redirect_to', {'url': '/wip/', 'permanent': False}),
    (r'^us/timeline/$', 'redirect_to', {'url': '/wip/', 'permanent': False}),
    (r'^us/gallery/$', 'redirect_to', {'url': '/wip/', 'permanent': False}),
    (r'^you/$', 'redirect_to', {'url': '/wip/', 'permanent': False}),
    (r'^you/parents/$', 'redirect_to', {'url': '/wip/', 'permanent': False}),
    (r'^you/witnesses/$', 'redirect_to', {'url': '/wip/', 'permanent': False}),
    (r'^wedding/celebration/$', 'redirect_to', {'url': '/wip/', 'permanent': False}),
    (r'^wedding/honeymoon/$', 'redirect_to', {'url': '/wip/', 'permanent': False}),
)

urlpatterns += patterns('',
    (r'^feeds/', include('feeds.urls')),
    (r'^lang/', include('django.conf.urls.i18n')),
    (r'^home/news/', include('news.urls')),
    (r'^you/polls/', include('polls.urls')),
    (r'^wedding/party/', include('confirm.urls')),
)
