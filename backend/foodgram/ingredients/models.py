from django.core.validators import MinValueValidator
from django.db import models


class Ingredient(models.Model):
    name = models.CharField(
        max_length=200,
    )
    measurement_unit = models.CharField(
        max_length=200,
    )


class IngredientInRecipe(models.Model):
    ingredients = models.ForeignKey(
        to=Ingredient,
        on_delete=models.CASCADE,
    )
    recipe = models.ForeignKey(
        to='recipes.Recipe',
        on_delete=models.CASCADE,
    )
    amount = models.PositiveIntegerField(
        validators=[
            MinValueValidator(
                1,
                message='Количество ингредиентов не может быть меньше 1!'
            )
        ]
    )