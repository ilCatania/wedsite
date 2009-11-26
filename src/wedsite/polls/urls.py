from django.conf.urls.defaults import patterns
from django.utils.translation import ugettext_lazy as _
import views
import models

urlpatterns = patterns('django.views.generic',
    (r'^$', 'simple.redirect_to', {'url': 'latest/', 'permanent': True}),
    (r'^latest/$', 'date_based.archive_index', 
        {'queryset': models.Poll.objects.all(), 
         'date_field': 'pub_date', 
         'num_latest': 5,
         'template_name': 'polls/list.djhtml',
         'extra_context': {'title': _('Latest polls')},
         'template_object_name':'polls'}),
    (r'^all/(?P<page>\d{1,}|(last))/$', 'list_detail.object_list', 
        {'queryset': models.Poll.objects.all(), 
         'paginate_by': 5, 
         'template_name': 'polls/list.djhtml',
         'extra_context': {'title': _('All polls')},
         'template_object_name':'polls'}),
    (r'^(?P<slug>[-\w]+)/$', 'list_detail.object_detail', 
        {'queryset': models.Poll.objects.all(),
         'template_name': 'polls/detail.djhtml',
         'template_object_name': 'poll'})
)
urlpatterns += patterns('',
    (r'^(?P<slug>[-\w]+)/form/$', views.show_form_ajax),
    (r'^(?P<slug>[-\w]+)/vote/$', views.vote_ajax),
    (r'^(?P<slug>[-\w]+)/results/$', views.show_results_ajax),
)