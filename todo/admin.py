from django.contrib import admin

from todo.models import Todo


@admin.register(Todo)
class TodoModelAdmin(admin.ModelAdmin):
    pass
