from django.db import models
import multilingual

class TodoList(models.Model):
    slug = models.SlugField(max_length=50, primary_key=True)
    class Translation(multilingual.Translation):
        description = models.TextField(max_length=1000)
    def __unicode__(self):
        return self.slug

class TodoItem(models.Model):
    parent_list = models.ForeignKey(TodoList)
    order = models.PositiveIntegerField(default=0)
    done = models.BooleanField(null=False, default=False)
    class Translation(multilingual.Translation):
        item_body = models.TextField(max_length=100)
    def __unicode__(self):
        return self.item_body[:10] + u'...'
    class Meta:
        ordering = ('order',)
        