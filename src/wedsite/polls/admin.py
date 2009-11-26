import models
from django.contrib import admin
import multilingual

class ChoiceInline(admin.StackedInline):
    model = models.Choice
    extra = 4
class SingleChoicePollAdmin(multilingual.ModelAdmin):
    inlines = [ChoiceInline]
    prepopulated_fields = {"slug": ("question_en",)}

class PercentagePollAdmin(multilingual.ModelAdmin):
    prepopulated_fields = {"slug": ("question_en",)}

admin.site.register(models.SingleChoicePoll, SingleChoicePollAdmin)
admin.site.register(models.PercentagePoll, PercentagePollAdmin)
admin.site.register(models.Choice, multilingual.ModelAdmin)
admin.site.register(models.Percentage, admin.ModelAdmin)
admin.site.register(models.LoggedVote, admin.ModelAdmin)