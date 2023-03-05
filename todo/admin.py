from django.contrib import admin

from todo.models import Tag
from todo.models import Todo


@admin.register(Todo)
class TodoModelAdmin(admin.ModelAdmin):
    pass


@admin.register(Tag)
class TagModelAdmin(admin.ModelAdmin):
    pass
