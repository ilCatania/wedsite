from django.contrib import admin
import models

class LoggedActionAdmin(admin.ModelAdmin):
    date_hierarchy = 'last_action'
    list_display = ('ip_addr', 'action_count', 'banned')
    list_filter = ('action_count', 'banned')

admin.site.register(models.LoggedAction, LoggedActionAdmin)
