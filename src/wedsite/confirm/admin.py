from django.contrib import admin
import models

class PartyConfirmationAdmin(admin.ModelAdmin):
    date_hierarchy = 'date_confirmed'
    list_display = ('name', 'adults', 'children', 'date_confirmed')

admin.site.register(models.PartyConfirmation, PartyConfirmationAdmin)

