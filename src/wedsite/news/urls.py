from django.conf.urls.defaults import patterns
from django.utils.translation import ugettext_lazy as _
import models

base_options = {'queryset': models.News.objects.all()}

latest_options = base_options.copy()
latest_options.update({'num_latest': 5, 'date_field': 'pub_date',
                       'template_name': 'news/list.djhtml',
                       'template_object_name':'news_items',
                       'extra_context': {'title': _('Latest news')}
                       })

all_options = base_options.copy()
all_options.update({'paginate_by': 5,
                    'template_name': 'news/all.djhtml',
                    'template_object_name':'news',
                    'extra_context': {'title': _('All news')}
                    })

detail_options = base_options.copy()
detail_options.update({'template_name': 'news/detail.djhtml',
                     'template_object_name': 'news_item'})

urlpatterns = patterns('django.views.generic',
    (r'^$', 'simple.redirect_to', {'url': 'latest/', 'permanent': True}),
    (r'^all/$', 'simple.redirect_to', {'url': '1/', 'permanent': True}),
    (r'^latest/$', 'date_based.archive_index', latest_options),
    (r'^all/(?P<page>\d{1,}|(last))/$', 'list_detail.object_list', all_options),
    (r'^(?P<slug>[-\w]+)/$', 'list_detail.object_detail', detail_options)
)
