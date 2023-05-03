from django.contrib import admin

from .models import Recipe


class RecipeAdmin(admin.ModelAdmin):
    fields = '__all__'


admin.site.register(Recipe)
