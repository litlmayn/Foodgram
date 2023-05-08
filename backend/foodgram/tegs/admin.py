from django.contrib import admin

from .models import Tag


class TagAdmin(admin.ModelAdmin):
    fields = ('id', 'name', 'color', 'slug')


admin.site.register(Tag)
