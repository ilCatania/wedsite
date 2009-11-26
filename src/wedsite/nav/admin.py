from models import Section
from django.contrib import admin
import multilingual

class SectionAdmin(multilingual.ModelAdmin):
        list_filter = ('parent',)
        list_display = ('name', 'slug', 'order', 'parent')
        search_fields = ('slug', 'name')

admin.site.register(Section, SectionAdmin)
