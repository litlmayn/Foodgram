import base64

from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from django.core.files.base import ContentFile


from tegs.models import Teg
from users.models import CustomUser
from ingredients.models import IngredientInRecipe, Ingredient
from recipes.models import Recipe
from subscriptions.models import Subscription
from favorites.models import Favorite


class Base64ImageField(serializers.ImageField):
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]
            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)

        return super().to_internal_value(data)


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = IngredientInRecipe
        fields = ('name', 'measurement_unit',)


class TegSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teg
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'email', 'first_name', 'last_name',)


class IngredientInRecipeSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source='ingredient.id')
    name = serializers.ReadOnlyField(source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measurement_unit')

    class Meta:
        model = IngredientInRecipe
        fields = ('id', 'name',
                  'measurement_unit', 'amount')


class RecipeSerializer(serializers.ModelSerializer):
    image = Base64ImageField(required=False)
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username',
    )
    ingredients = IngredientInRecipeSerializer(
        many=True, read_only=True, source='recipes'
    )
    tags = TegSerializer(many=True, read_only=True)

    class Meta:
        model = Recipe
        fields = (
            'id', 'tags', 'author',
            'ingredients', 'name', 'image',
            'text', 'cooking_time',
        )
        depth = 1

    def create(self, validated_data):
        tags = validated_data.pop('tags')
        ingredients = validated_data.pop('ingredients')
        recipe = Recipe.objects.create(author=self.context['request'].user,
                                       **validated_data)
        self.tags_and_ingredients_set(recipe, tags, ingredients)
        return recipe


class SubscriptionSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(
        slug_field='id',
        queryset=CustomUser.objects.all(),
    )
    following = serializers.SlugRelatedField(
        slug_field='id',
        queryset=CustomUser.objects.all(),
    )

    def validate_subscribe(self, following):
        if self.context['request'].user != following:
            return following
        raise serializers.ValidationError("Нельзя подписаться на самого себя!")

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
        read_only=True,
        slug_field='id',
    )
    recipe = serializers.SlugRelatedField(
        read_only=True,
        slug_field='id',
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
