from django.db import models
from django.core.cache import cache
import multilingual

class NavManager(multilingual.Manager):
    def main_sections(self):
        return self.filter(parent__isnull=True)

class Section(models.Model):
    slug   = models.SlugField(max_length=12)
    class Translation(multilingual.Translation):
        name   = models.CharField(max_length=50)
    order  = models.IntegerField(default=0)
    parent = models.ForeignKey('self', related_name='children',
                               blank=True, null=True)
    objects = NavManager()
    def __unicode__(self):
        return self.name

    def save(self):
        cache.delete('site_navtree')
        return super(Section, self).save()
    class Meta:
        ordering = ('parent__id', 'order', 'slug')


def build_sitemap():
    def build(ent, parent):
        url = '/' + ent.slug + '/'
        if(parent): 
            url = '/' + parent.slug + url
            children = []
        else:
            children = [build(c, ent) for c in ent.children.all()]
        return {'slug': ent.slug, 'name': ent.name, 'url': url, 'selected': False, 
                'parent': parent, 'children': children}
    return [build(ent, None) for ent in Section.objects.main_sections()]

def get_sitemap():
    cachename = 'site_navtree'
    timeout = 60*60*24*7
    data = cache.get(cachename)
    if data is None:
        data = build_sitemap()
        cache.set(cachename, data, timeout)
    return data
