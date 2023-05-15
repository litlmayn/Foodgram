from django.contrib import admin

from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'first_name',
                    'last_name', 'in_subscribe', 'in_recipe')
    search_fields = ('email', 'username',)

    def in_recipe(self, obj):
        return obj.author.all().count()
    in_recipe.short_description = 'Количество рецептов автора'

    def in_subscribe(self, obj):
        return obj.following.all().count()
    in_subscribe.short_description = 'Количество подписчиков'
