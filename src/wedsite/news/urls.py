from django.conf.urls.defaults import patterns
from django.utils.translation import ugettext_lazy as _
import models

urlpatterns = patterns('django.views.generic',
    (r'^$', 'simple.redirect_to', {'url': 'latest/', 'permanent': True}),
    (r'^latest/$', 'date_based.archive_index', 
        {'queryset': models.News.objects.all(), 
         'date_field': 'pub_date', 
         'num_latest': 5,
         'template_name': 'news/list.djhtml',
         'extra_context': {'title': _('Latest news')},
         'template_object_name':'news_items'}),
    (r'^all/(?P<page>\d{1,}|(last))$', 'list_detail.object_list', 
        {'queryset': models.News.objects.all(), 
         'paginate_by': 5, 
         'template_name': 'news/list.djhtml',
         'extra_context': {'title': _('All news')},
         'template_object_name':'news_items'}),
    (r'^(?P<slug>[-\w]+)/$', 'list_detail.object_detail', 
        {'queryset': models.News.objects.all(),
         'template_name': 'news/detail.djhtml',
         'template_object_name': 'newsitem'})
)
