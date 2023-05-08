from django.core.validators import MinValueValidator
from django.db import models

from users.models import CustomUser
from tegs.models import Tag
from ingredients.models import Ingredient


class Recipe(models.Model):
    author = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='author',
        verbose_name='Автор рецепта',

    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата публикации',
    )
    name = models.CharField(
        max_length=200,
        verbose_name='Название рецепта',
    )
    image = models.ImageField(
        'Картинка',
        upload_to='recipes/media/',
    )
    text = models.TextField(
        verbose_name='Текст рецепта',
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        through='ingredients.IngredientInRecipe',
    )
    tags = models.ForeignKey(Tag, on_delete=models.DO_NOTHING)
    cooking_time = models.PositiveIntegerField(
        validators=[
            MinValueValidator(
                1,
                message='Время не может быть меньше 1 минуты!'
            )
        ],
        verbose_name='Время приготовления',
    )
    is_favorited = models.BooleanField(default=False)
    is_in_shopping_cart = models.BooleanField(default=False)
