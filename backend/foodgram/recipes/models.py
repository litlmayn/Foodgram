from django.core.validators import MinValueValidator, RegexValidator
from django.db import models

from users.models import CustomUser


class Tag(models.Model):
    name = models.CharField(
        unique=True,
        max_length=200,
    )
    color = models.CharField(
        max_length=7,
        unique=True,
        help_text='Введите уникальный цвет в формате HEX',
        verbose_name='Цвет в HEX',
        validators=[RegexValidator(regex='^#[A-Fa-f0-9]{6}$',
                                   message='Неверный HEX-код')]
    )
    slug = models.SlugField(
        unique=True,
        max_length=200,
    )

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    name = models.CharField(
        max_length=200,
        db_index=True,
    )
    measurement_unit = models.CharField(
        max_length=200,
    )


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
    cooking_time = models.PositiveIntegerField(
        verbose_name='Время приготовления',
        validators=[
            MinValueValidator(
                1,
                message='Время не может быть меньше 1 минуты!'
            )
        ],
    )


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
    amount = models.PositiveIntegerField(
        verbose_name='Количество',
        validators=[
            MinValueValidator(
                1,
                message='Количество ингредиентов не может быть меньше 1!'
            )
        ]
    )


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

    class Meta:
        verbose_name = 'Избранные рецепты.'


class Subscription(models.Model):
    user = models.ForeignKey(
        'users.CustomUser',
        on_delete=models.CASCADE,
        related_name='follower',
    )
    following = models.ForeignKey(
        'users.CustomUser',
        on_delete=models.CASCADE,
        related_name='following',
    )

    def __str__(self):
        return f'{self.user}, {self.following}'

    class Meta:
        verbose_name = 'Подписка на авторов.'


class ShoppingCart(models.Model):
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

    class Meta:
        default_related_name = 'shopping_cart'
        verbose_name = 'Список покупок.'
