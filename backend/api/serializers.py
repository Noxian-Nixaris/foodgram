from django.contrib.auth import get_user_model
from djoser.serializers import UserSerializer as BaseUserSerializer
from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers

from users_authentication.models import UserSubscription
from foodgram.models import (
    Ingredient,
    Favorite,
    Recipe,
    RecipeIngredient,
    RecipeTag,
    ShoppingCart,
    Tag
)


User = get_user_model()


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = ('id', 'name', 'slug')


class IngredientSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit')


class IngredientRecipeSerializer(serializers.ModelSerializer):
    id = serializers.SlugRelatedField(
        slug_field='id',
        queryset=Ingredient.objects.all()
    )
    name = serializers.SlugRelatedField(
        slug_field='ingredient__name',
        read_only=True
    )
    measurement_unit = serializers.SlugRelatedField(
        slug_field='ingredient__measurement_unit',
        read_only=True
    )

    class Meta:
        model = RecipeIngredient
        fields = ('id', 'name', 'measurement_unit', 'amount')


class ShortRecipeSerializer(serializers.ModelSerializer):
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')


class UserSerializer(BaseUserSerializer):
    is_subscribed = serializers.SerializerMethodField()
    avatar = Base64ImageField(required=False, allow_null=True)

    class Meta(BaseUserSerializer.Meta):
        model = User
        fields = [
            'email', 'id', 'username',
            'first_name', 'last_name',
            'is_subscribed', 'avatar'
        ]

    def get_is_subscribed(self, obj):
        user = self.context['request'].user
        return UserSubscription.objects.filter(
            user=user, subscribed=obj
        ).exists()


class SubscriptionSerializer(UserSerializer):
    recipes = ShortRecipeSerializer(many=True)
    recipes_count = serializers.SerializerMethodField()

    class Meta(UserSerializer.Meta):
        model = User
        fields = [
            'email', 'id', 'username',
            'first_name', 'last_name',
            'is_subscribed', 'recipes',
            'recipes_count', 'avatar'
        ]

    def get_recipes_count(self, obj):
        return Recipe.objects.filter(author=obj.pk).count()


class RecipeSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True)
    author = UserSerializer(read_only=True)
    ingredients = IngredientRecipeSerializer(many=True)
    image = Base64ImageField()
    is_favorite = serializers.SerializerMethodField(
        'get_is_favorite',
        read_only=True
    )
    is_in_shopping_cart = serializers.SerializerMethodField(
        'get_is_in_shopping_cart',
        read_only=True
    )

    class Meta:
        model = Recipe
        fields = (
            'id', 'tags', 'author', 'ingredients',
            'is_favorite', 'is_in_shopping_cart',
            'name', 'image', 'text', 'cooking_time'
        )

    def get_is_favorite(self, obj):
        return Favorite.objects.filter(
            user=self.context['request'].user, favorite=obj.pk
        ).exists()

    def get_is_in_shopping_cart(self, obj):
        return ShoppingCart.objects.filter(
            user=self.context['request'].user, recipe=obj.pk
        ).exists()


class RecipeCreateSerializer(serializers.ModelSerializer):
    tags = serializers.SlugRelatedField(
        slug_field='pk',
        queryset=Tag.objects.all(),
        many=True)
    author = UserSerializer(read_only=True)
    ingredients = IngredientRecipeSerializer(many=True)
    image = Base64ImageField()
    is_favorite = serializers.SerializerMethodField(
        'get_is_favorite',
        read_only=True
    )
    is_in_shopping_cart = serializers.SerializerMethodField(
        'get_is_in_shopping_cart',
        read_only=True
    )

    class Meta:
        model = Recipe
        fields = (
            'id', 'tags', 'author', 'ingredients',
            'is_favorite', 'is_in_shopping_cart',
            'name', 'image', 'text', 'cooking_time'
        )

    def create(self, validated_data):
        tags_data = validated_data.pop('tags')
        ingredients_data = validated_data.pop('ingredients')
        data = Recipe.objects.create(
            author=self.context['request'].user, **validated_data
        )

        tag_set = (
            RecipeTag(recepe=data, tag=tag) for tag in tags_data
        )
        tags = RecipeTag.objects.bulk_create(tag_set)
        ingredient_set = (
            RecipeIngredient(
                recipe=data,
                ingredient=Ingredient.objects.filter(pk=ingredient),
                amount=amount['amount']
            ) for ingredient, amount in ingredients_data
        )
        ingredients = RecipeIngredient.objects.bulk_create(ingredient_set)

        data = Recipe.objects.create(
            tags=tags, ingredients=ingredients, **validated_data
        )
        for ingridient, amount in ingredients_data:
            RecipeIngredient.objects.filter(
                recipe=data, ingridient=ingridient).update(amount=amount)
        return Recipe.objects.filter(pk=data.pk)

