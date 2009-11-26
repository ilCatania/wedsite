from django.conf.urls.defaults import patterns
import models
feeds = {
    'latest-en': models.LatestEntriesEn,
    'latest-it': models.LatestEntriesIt,
}

urlpatterns = patterns('',
    (r'^(?P<url>.*)/$', 'django.contrib.syndication.views.feed', {'feed_dict': feeds}),
)
