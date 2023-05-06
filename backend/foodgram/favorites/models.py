from django.db import models


class Favorite(models.Model):
    user = models.ForeignKey(
        'users.CustomUser',
        on_delete=models.CASCADE
    )
    recipe = models.ForeignKey(
        'recipes.Recipe',
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return f'{self.user}, {self.recipe}'
