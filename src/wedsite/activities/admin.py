import models
from django.contrib import admin
import multilingual

class TodoListAdmin(multilingual.ModelAdmin):
    list_display = ('slug', 'description')

class TodoItemAdmin(multilingual.ModelAdmin):
    list_display = ('item_body',)

admin.site.register(models.TodoList, TodoListAdmin)
admin.site.register(models.TodoItem, TodoItemAdmin)
