from django.db import models
from django.core.cache import cache
from django.contrib.auth.models import User
import multilingual

class NewsManager(multilingual.Manager):
    pass

class News(models.Model):
    slug   = models.SlugField(max_length=24)
    pub_date  = models.DateTimeField()
    author = models.ForeignKey(User)
    class Translation(multilingual.Translation):
        title = models.CharField(max_length=100)
        text = models.TextField(max_length=2000)
    objects = NewsManager()
    def __unicode__(self):
        return self.slug
    def save(self):
        cache.delete('news_latest')
        cache.delete('news_all')
        return super(News, self).save()
    class Meta:
        ordering = ('-pub_date', 'slug',)
    