from django.conf import settings
from django.contrib.auth import get_user_model
from djoser.serializers import UserSerializer as BaseUserSerializer
from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers, exceptions
from rest_framework.generics import get_object_or_404

from core.validators import (
    amount_validation,
    not_empty_validation,
    positive_check
)
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
    id = serializers.ReadOnlyField(source='ingredient.id')
    name = serializers.ReadOnlyField(source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measurement_unit'
    )

    class Meta:
        model = RecipeIngredient
        fields = ('id', 'name', 'measurement_unit', 'amount',)


class IngredientRecipeCreateSerializer(serializers.ModelSerializer):
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

    def validate(self, data):
        recipe = self.context['recipe']
        user = self.context['request'].user
        try:
            ShoppingCart.objects.create(user=user, recipe=recipe)
        except Exception:
            raise serializers.ValidationError()
        return data


class FavoriteRecipeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')
        read_only_fields = ('id', 'name', 'image', 'cooking_time')

    def validate(self, data):
        recipe = self.context['recipe']
        user = self.context['request'].user
        try:
            Favorite.objects.create(user=user, favorite=recipe)
        except Exception:
            raise serializers.ValidationError()
        return data


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
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()

    class Meta(UserSerializer.Meta):
        model = User
        fields = [
            'email', 'id', 'username',
            'first_name', 'last_name',
            'is_subscribed', 'recipes',
            'recipes_count', 'avatar'
        ]

    def get_recipes(self, obj):
        recipes = Recipe.objects.filter(author=obj.pk)
        params = self.context.get('request').query_params
        if 'recipes_limit' in params:
            recipes = recipes[:int(params.get('recipes_limit'))]
        serializer = ShortRecipeSerializer(recipes, many=True)
        return serializer.data

    def get_recipes_count(self, obj):
        return Recipe.objects.filter(author=obj.pk).count()

    def validate(self, data):
        user = self.context['request'].user
        sub = self.context['sub']
        if user == sub:
            raise serializers.ValidationError()
        try:
            UserSubscription.objects.create(user=user, subscribed=sub)
        except Exception:
            raise serializers.ValidationError()
        return data

    # def create(self, validated_data):
    #     print(validated_data)
    #     user = self.context['request'].user
    #     sub = self.kwargs['id']
    #     print(sub, '***')
    #     subscription = UserSubscription.objects.create(user=user, subscribed=sub)
    #     return subscription


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
        slug_field='id',
        queryset=Tag.objects.all(),
        many=True)
    author = UserSerializer(read_only=True)
    ingredients = IngredientRecipeCreateSerializer(
        source='recipes_ingredients',
        many=True
    )
    image = Base64ImageField()
    is_favorited = serializers.SerializerMethodField(
        'get_is_favorited',
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
            'is_favorited', 'is_in_shopping_cart',
            'name', 'image', 'text', 'cooking_time'
        )

    def validate(self, data):
        try:
            tags_data = data['tags']
        except Exception:
            print('tags')
            raise serializers.ValidationError()
        amount_validation(tags_data)

        try:
            ingredients_data = data['recipes_ingredients']
        except Exception:
            print('recipes_ingredients')
            raise serializers.ValidationError()
        ingredients = [data.get('id') for data in ingredients_data]
        amount_validation(ingredients)

        try:
            image = data['image']
        except Exception:
            print('image')
            raise serializers.ValidationError()
        not_empty_validation(image)

        try:
            cooking_time = data['cooking_time']
        except Exception:
            print('cooking_time')
            raise serializers.ValidationError()
        positive_check(cooking_time)

        return data

    def create(self, validated_data):
        tags_data = validated_data.pop('tags')
        ingredients_data = validated_data.pop('recipes_ingredients')
        if not self.context['request'].user.is_authenticated:
            raise exceptions.NotAuthenticated()
        recipe = Recipe.objects.create(
            author=self.context['request'].user, **validated_data
        )
        recipe.tags.set(tags_data)
        ingredient_set = (
            RecipeIngredient(
                recipe=recipe,
                ingredient=value.get('id'),
                amount=value.get('amount')
            ) for value in ingredients_data
        )
        RecipeIngredient.objects.bulk_create(ingredient_set)
        return recipe

    def update(self, instance, validated_data):
        tags_data = validated_data.pop('tags')
        instance.tags.clear()
        instance.tags.set(tags_data)
        ingredients_data = validated_data.pop('recipes_ingredients')
        RecipeIngredient.objects.filter(recipe=instance).delete()
        ingredient_set = (
            RecipeIngredient(
                recipe=instance,
                ingredient=value.get('id'),
                amount=value.get('amount')
            ) for value in ingredients_data
        )
        RecipeIngredient.objects.bulk_create(ingredient_set)
        Recipe.objects.filter(pk=instance.pk).update(**validated_data)
        return get_object_or_404(Recipe, pk=instance.pk)

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

    def to_representation(self, instance):
        data = super(RecipeCreateSerializer, self).to_representation(instance)
        data['ingredients'] = IngredientRecipeSerializer(
            instance.recipes_ingredients.all(), many=True
        ).data
        data['tags'] = TagSerializer(instance.tags.all(), many=True).data
        return data


class ShortURLSerializer(serializers.ModelSerializer):
    short_link = serializers.SerializerMethodField()

    class Meta:
        model = ShortURL
        fields = ('short_link',)

    def get_short_link(self, obj):
        return f'{settings.DOMAIN}s/{obj.short_link}'

    def to_representation(self, instance):
        fields = self._readable_fields
        for field in fields:
            if field.field_name == 'short_link':
                field.field_name = 'short-link'
        return super().to_representation(instance)


class AvatarSerializer(BaseUserSerializer):
    avatar = Base64ImageField(required=False, allow_null=True)

    class Meta(BaseUserSerializer.Meta):
        model = User
        fields = ('avatar',)

    def validate(self, data):
        if 'avatar' not in data or data.get('avatar') is None:
            raise serializers.ValidationError()
        return data
