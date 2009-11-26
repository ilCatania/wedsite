from models import News
from django.contrib import admin
import multilingual

class NewsAdmin(multilingual.ModelAdmin):
    date_hierarchy = 'pub_date'
    list_display = ('slug', 'title')
    list_filter = ('author', 'pub_date')
    prepopulated_fields = {"slug": ("title_en",)}

admin.site.register(News, NewsAdmin)

