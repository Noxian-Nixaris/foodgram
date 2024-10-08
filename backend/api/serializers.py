from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from djoser.serializers import UserSerializer as BaseUserSerializer
from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers
from core.constants import DOMAIN
from foodgram.models import (
    Favorite,
    Ingredient,
    Recipe,
    RecipeIngredient,
    ShoppingCart,
    ShortURL,
    Tag
)
from users_authentication.models import UserSubscription


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
    id = serializers.PrimaryKeyRelatedField(queryset=Ingredient.objects.all())
    name = serializers.ReadOnlyField(source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measurement_unit'
    )

    class Meta:
        model = RecipeIngredient
        fields = ('id', 'name', 'measurement_unit', 'amount',)


class ShortRecipeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')
        read_only_fields = ('id', 'name', 'image', 'cooking_time')


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
        if user.is_authenticated:
            return UserSubscription.objects.filter(
                user=user, subscribed=obj
            ).exists()
        return False


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
    ingredients = IngredientRecipeSerializer(
        source='recipes_ingredients',
        many=True,
        read_only=True
    )
    image = Base64ImageField()
    is_favorited = serializers.SerializerMethodField(
        read_only=True
    )
    is_in_shopping_cart = serializers.SerializerMethodField(
        read_only=True
    )

    class Meta:
        model = Recipe
        fields = (
            'id', 'tags', 'author', 'ingredients',
            'is_favorited', 'is_in_shopping_cart',
            'name', 'image', 'text', 'cooking_time'
        )

    def get_is_favorited(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            return Favorite.objects.filter(
                user=user, favorite=obj.pk
            ).exists()
        return False

    def get_is_in_shopping_cart(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            return ShoppingCart.objects.filter(
                user=user, recipe=obj.pk
            ).exists()
        return False


class RecipeCreateSerializer(serializers.ModelSerializer):
    tags = serializers.SlugRelatedField(
        slug_field='pk',
        queryset=Tag.objects.all(),
        many=True)
    author = UserSerializer(read_only=True)
    ingredients = IngredientRecipeSerializer(
        source='recipes_ingredients', many=True
    )
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
        ingredients_data = validated_data.pop('recipes_ingredients')

        tag_set = [tag for tag in tags_data]
        data = Recipe.objects.create(
            author=self.context['request'].user, **validated_data
        )
        recipe = get_object_or_404(Recipe, pk=data.pk)
        recipe.tags.set(tag_set)
        ingredient_set = (
            RecipeIngredient(
                recipe=recipe,
                ingredient=value.get('id'),
                amount=value.get('amount')
            ) for value in ingredients_data
        )
        RecipeIngredient.objects.bulk_create(ingredient_set)
        return get_object_or_404(Recipe, pk=recipe.pk)

    def get_is_favorite(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            return Favorite.objects.filter(
                user=user, favorite=obj.pk
            ).exists()
        return False

    def get_is_in_shopping_cart(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            return ShoppingCart.objects.filter(
                user=user, recipe=obj.pk
            ).exists()
        return False


class ShortURLSerializer(serializers.ModelSerializer):
    short_link = serializers.SerializerMethodField()

    class Meta:
        model = ShortURL
        fields = ('short_link',)

    def get_short_link(self, obj):
        return f'{DOMAIN}s/{obj.short_link}'

    def to_representation(self, instance):
        fields = self._readable_fields
        for field in fields:
            if field.field_name == 'short_link':
                field.field_name = 'short-link'
        return super().to_representation(instance)
