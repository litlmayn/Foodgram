from colorfield.fields import ColorField
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

from api.constants import RECIPE_MAX_LENGHT
from users.models import CustomUser


class Tag(models.Model):
    name = models.CharField(
        unique=True,
        max_length=RECIPE_MAX_LENGHT,
        verbose_name='Название тега',
    )
    color = ColorField(
        default='#FF0000',
        verbose_name='Цвет тега',
    )
    slug = models.SlugField(
        unique=True,
        max_length=RECIPE_MAX_LENGHT,
        verbose_name='Slug тега'
    )

    class Meta:
        verbose_name = 'Тэги'

    def __str__(self):
        return f'{self.name}'


class Ingredient(models.Model):
    name = models.CharField(
        max_length=RECIPE_MAX_LENGHT,
        db_index=True,
        verbose_name='Название ингредиента',
    )
    measurement_unit = models.CharField(
        max_length=RECIPE_MAX_LENGHT,
        verbose_name='Единицы измерения',
    )

    class Meta:
        verbose_name = 'Ингредиенты',
        constraints = (
            models.UniqueConstraint(
                fields=('name', 'measurement_unit'),
                name='unique_ingredient'
            ),
        )

    def __str__(self) -> str:
        return f'{self.name}'


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
        max_length=RECIPE_MAX_LENGHT,
        verbose_name='Название рецепта',
    )
    image = models.ImageField(
        verbose_name='Картинка',
        upload_to='recipes/media/',
    )
    text = models.TextField(
        verbose_name='Текст рецепта',
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        through='IngredientInRecipe',
        verbose_name='Ингредиенты',
    )
    tags = models.ManyToManyField(
        Tag,
        verbose_name='Теги',
        related_name='tags',
    )
    cooking_time = models.PositiveSmallIntegerField(
        verbose_name='Время приготовления',
        validators=[
            MinValueValidator(
                1,
                message='Время не может быть меньше 1 минуты!'
            ),
            MaxValueValidator(
                300,
                message='Время готовки не должно быть больше 300 минут!'
            )
        ],
    )

    class Meta:
        verbose_name = 'Рецепт'
        ordering = ['name', 'author']

    def __str__(self):
        return f'{self.name}'


class IngredientInRecipe(models.Model):
    ingredients = models.ForeignKey(
        to=Ingredient,
        on_delete=models.CASCADE,
        verbose_name='Ингредиент',
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='recipe_ingredients',
        verbose_name='Рецепт',
    )
    amount = models.PositiveSmallIntegerField(
        verbose_name='Количество',
        validators=[
            MinValueValidator(
                1,
                message='Количество ингредиентов не может быть меньше 1!'
            ),
            MaxValueValidator(
                10000,
                message='Количество ингредиентов слишком большое!'
            )
        ]
    )

    class Meta:
        verbose_name = 'Ингредиенты в рецепте'

    def __str__(self) -> str:
        return f'{self.recipe}'


class Subscription(models.Model):
    user = models.ForeignKey(
        'users.CustomUser',
        on_delete=models.CASCADE,
        related_name='follower',
        verbose_name='Подписчик',
    )
    following = models.ForeignKey(
        'users.CustomUser',
        on_delete=models.CASCADE,
        related_name='following',
        verbose_name='Фолловер',
    )

    class Meta:
        verbose_name = 'Подписка на авторов.'
        ordering = ['following']
        constraints = (
            models.UniqueConstraint(
                fields=('user', 'following'),
                name='unique_following'
            ),
            models.CheckConstraint(
                check=~models.Q(user=models.F('following')),
                name='no_self_following'
            )
        )

    def __str__(self):
        return f'{self.user}, {self.following}'


class UserRecipe(models.Model):
    user = models.ForeignKey(
        'users.CustomUser',
        on_delete=models.CASCADE,
        verbose_name='Пользователь'
    )
    recipe = models.ForeignKey(
        'recipes.Recipe',
        on_delete=models.CASCADE,
        verbose_name='Рецепт'
    )

    class Meta:
        abstract = True
        ordering = ['recipe']

    def __str__(self):
        return f'{self.recipe}, {self.user}'


class Favorite(UserRecipe):

    class Meta:
        verbose_name = 'Избранные рецепты'
        default_related_name = 'favorite'
        constraints = (
            models.UniqueConstraint(
                fields=('user', 'recipe'),
                name='unique_favorite'
            ),
        )


class ShoppingCart(UserRecipe):

    class Meta:
        verbose_name = 'Список покупок'
        default_related_name = 'shopping_cart'
        constraints = (
            models.UniqueConstraint(
                fields=('user', 'recipe'),
                name='unique_cart'
            ),
        )
