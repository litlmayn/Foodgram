from django.shortcuts import get_object_or_404
from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.validators import UniqueTogetherValidator

from recipes.models import (Favorite, Ingredient, IngredientInRecipe, Recipe,
                            ShoppingCart, Subscription, Tag)
from users.models import CustomUser


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit',)


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'email', 'first_name',
                  'last_name', 'password', 'is_subscribed')
        extra_kwargs = {'password': {'write_only': True},
                        'is_subscribed': {'read_only': True}}

    def get_is_subscribed(self, obj):
        requset = self.context.get('request')
        return (requset and
                not requset.user.is_anonymous and
                CustomUser.objects.filter(following=obj.id).exists())

    # без этого метода у меня пароль не хешируется
    def create(self, validated_data):
        return CustomUser.objects.create_user(**validated_data)


class IngredientInRecipeSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(queryset=Ingredient.objects.all())
    amount = serializers.IntegerField()

    class Meta:
        model = IngredientInRecipe
        fields = ('id', 'amount')


class RecipeIngredientSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source='ingredients.id')
    name = serializers.ReadOnlyField(source='ingredients.name')
    measurement_unit = serializers.ReadOnlyField(
        source='ingredients.measurement_unit')

    class Meta:
        model = IngredientInRecipe
        fields = ('id', 'name', 'measurement_unit', 'amount')


class RecipeListSerializer(serializers.ModelSerializer):
    tags = TagSerializer(read_only=True, many=True)
    author = UserSerializer(read_only=True)
    ingredients = RecipeIngredientSerializer(
        read_only=True,
        many=True,
        source='recipe_ingredients'
    )
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = ('id', 'tags', 'author', 'ingredients', 'is_favorited',
                  'is_in_shopping_cart', 'name', 'image', 'text',
                  'cooking_time')

    def get_is_favorited(self, obj):
        request = self.context.get('request')
        return (
            request and
            not request.user.is_anonymous and
            CustomUser.objects.filter(favorite__recipe=obj.id).exists()
        )

    def get_is_in_shopping_cart(self, obj):
        request = self.context.get('request')
        return (
            request and
            not request.user.is_anonymous and
            CustomUser.objects.filter(shopping_cart__recipe=obj.id).exists()
        )


class RecipeAddSerializer(serializers.ModelSerializer):
    image = Base64ImageField()
    author = serializers.HiddenField(
        default=serializers.CurrentUserDefault())
    ingredients = IngredientInRecipeSerializer(
        many=True, write_only=True,
    )
    tags = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Tag.objects.all(),
    )
    cooking_time = serializers.IntegerField()

    class Meta:
        model = Recipe
        fields = (
            'id', 'tags', 'author',
            'ingredients', 'name', 'image',
            'text', 'cooking_time',
        )

    @staticmethod
    def create_tag_ingredient(ingredients, tags, model):
        recipe_ingredients = [
            IngredientInRecipe(recipe=model,
                               ingredients=ingredient['id'],
                               amount=ingredient['amount'])
            for ingredient in ingredients
        ]
        IngredientInRecipe.objects.bulk_create(recipe_ingredients)
        model.tags.set(tags)

    def create(self, validated_data):
        tags = validated_data.pop('tags')
        ingredients = validated_data.pop('ingredients')
        recipe = super().create(validated_data)
        self.create_tag_ingredient(ingredients, tags, recipe)
        return recipe

    def update(self, instance, validated_data):
        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')
        instance.ingredients.clear()
        self.create_tag_ingredient(ingredients, tags, instance)
        return super().update(instance, validated_data)

    def validate_ingredients(self, value):
        if not value:
            raise ValidationError(
                {'ingredients': 'Необходимо выбрать ингредиент'})
        ingredients_list = []
        for item in value:
            ingredient = get_object_or_404(Ingredient, name=item['id'])
            if ingredient in ingredients_list:
                raise ValidationError(
                    {'ingredients': 'Ингридиенты не должны повторяться'})
            ingredients_list.append(ingredient)
        return value

    def validate_tags(self, value):
        if not value:
            raise ValidationError(
                {'tags': 'Необходимо выбрать тег'})
        tags_list = []
        for tag in value:
            if tag in tags_list:
                raise ValidationError(
                    {'tags': 'Теги не должны повторяться'})
            tags_list.append(tag)
        return value

    def to_representation(self, instance):
        return RecipeListSerializer(instance, context=self.context).data


class RecipeForSubSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')


class SubscribeSerializer(serializers.ModelSerializer):
    email = serializers.ReadOnlyField(source='following.email')
    id = serializers.ReadOnlyField(source='following.id')
    username = serializers.ReadOnlyField(source='following.username')
    first_name = serializers.ReadOnlyField(source='following.first_name')
    last_name = serializers.ReadOnlyField(source='following.last_name')
    is_subscribed = serializers.SerializerMethodField()
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()

    class Meta:
        model = Subscription
        fields = ('email', 'id', 'username', 'first_name', 'last_name',
                  'is_subscribed', 'recipes', 'recipes_count')

    def get_is_subscribed(self, obj):
        requset = self.context.get('request')
        return (requset and
                not requset.user.is_anonymous and
                CustomUser.objects.filter(following=obj.id).exists())

    def get_recipes(self, obj):
        request = self.context.get('request')
        limit = request.GET.get('recipes_limit')
        recipes = Recipe.objects.filter(author__following=obj.id)
        if limit and limit.isdigit():
            recipes = recipes[:int(limit)]
        return RecipeForSubSerializer(recipes, many=True).data

    def get_recipes_count(self, obj):
        return Recipe.objects.filter(author__following=obj.id).count()


class SubscriptionSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(
        slug_field='id',
        queryset=CustomUser.objects.all(),
    )
    following = serializers.SlugRelatedField(
        slug_field='id',
        queryset=CustomUser.objects.all(),
    )

    def validate(self, data):
        if data['user'] == data['following']:
            raise serializers.ValidationError(
                "Нельзя подписаться на самого себя!"
            )
        return data

    class Meta:
        model = Subscription
        fields = ('user', 'following',)
        validators = [
            UniqueTogetherValidator(
                queryset=Subscription.objects.all(),
                fields=['user', 'following'],
                message=('Вы уже подписались на данного автора!'),
            ),
        ]


class FavoriteSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(
        slug_field='id',
        queryset=CustomUser.objects.all(),
    )
    recipe = serializers.SlugRelatedField(
        slug_field='id',
        queryset=Recipe.objects.all()
    )

    class Meta:
        model = Favorite
        fields = ('user', 'recipe',)
        validators = [
            UniqueTogetherValidator(
                queryset=Favorite.objects.all(),
                fields=('user', 'recipe',),
                message=('Вы уже добавили данный рецепт в избранное!'),
            ),
        ]


class ShoppingCartSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(
        slug_field='id',
        queryset=CustomUser.objects.all(),
    )
    recipe = serializers.SlugRelatedField(
        slug_field='id',
        queryset=Recipe.objects.all()
    )

    class Meta:
        model = ShoppingCart
        fields = ('user', 'recipe',)
        validators = [
            UniqueTogetherValidator(
                queryset=ShoppingCart.objects.all(),
                fields=('user', 'recipe',),
                message=('Вы уже добавили данный рецепт в список покупок!'),
            ),
        ]
