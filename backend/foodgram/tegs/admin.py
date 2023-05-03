from django.contrib import admin

from .models import Teg


class TegAdmin(admin.ModelAdmin):
    fields = ('id', 'name', 'color', 'slug')


admin.site.register(Teg)
