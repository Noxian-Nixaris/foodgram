from django.contrib.auth import get_user_model
from django.db import models
from core.constants import MAX_DISPLAY_LENGTH, MAX_LENGTH
from core.validators import time_check

User = get_user_model()


class Tag(models.Model):
    name = models.CharField(
        max_length=MAX_LENGTH,
        unique=True,
        verbose_name='Название'
    )
    slug = models.SlugField(unique=True, verbose_name='Слаг')

    class Meta:
        default_related_name = 'tag'
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    name = models.CharField(
        max_length=MAX_LENGTH,
        unique=True,
        verbose_name='Название'
    )
    measurement_unit = models.CharField(
        max_length=MAX_LENGTH,
        verbose_name='Единица измерения'
    )

    class Meta:
        default_related_name = 'ingredients'
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'
        ordering = ('name', 'id')

    def __str__(self):
        return self.name


class Recipe(models.Model):
    name = models.CharField(max_length=MAX_LENGTH, verbose_name='Название')
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор'
    )
    image = models.ImageField(
        upload_to='recipes/',
        null=True,
        default=None,
        verbose_name='Изображение'
    )
    text = models.TextField(verbose_name='Описание')
    ingredients = models.ManyToManyField(
        Ingredient,
        through='RecipeIngredient',
        verbose_name='Ингридиенты'
    )
    tags = models.ManyToManyField(
        Tag,
        through='RecipeTag',
        verbose_name='Теги'
    )
    cooking_time = models.SmallIntegerField(
        validators=[time_check],
        verbose_name='Время приготовления'
    )
    is_in_shopping_cart = models.ManyToManyField(
        User,
        through='ShoppingCart',
        verbose_name='Покупки',
        related_name='is_in_shopping_cart'
    )
    is_favorited = models.ManyToManyField(
        User,
        through='Favorite',
        verbose_name='Избранное',
        related_name='is_favorited'
    )

    class Meta:
        default_related_name = 'recipes'
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'
        ordering = ('name', 'id')

    def __str__(self):
        return self.name[:MAX_DISPLAY_LENGTH]


class RecipeTag(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.recipe} {self.tag}'

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=('recipe', 'tag'), name='tag_recipe'
            )
        ]


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    amount = models.IntegerField(
        null=True, verbose_name='Количество'
    )

    class Meta:
        default_related_name = 'recipes_ingredients'
        constraints = [
            models.UniqueConstraint(
                fields=('recipe', 'ingredient'), name='ingredient_recipe'
            )
        ]


class Favorite(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )
    favorite = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE
    )

    class Meta:
        default_related_name = 'favotrite'
        constraints = [
            models.UniqueConstraint(
                fields=('user', 'favorite'), name='favorite_recipe'
            )
        ]

    def __str__(self):
        return f'{self.user} {self.favorite}'


class ShoppingCart(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE
    )

    class Meta:
        default_related_name = 'shopping_cart'
        constraints = [
            models.UniqueConstraint(
                fields=('user', 'recipe'), name='shopping_cart'
            )
        ]


class ShortURL(models.Model):
    full_link = models.CharField(max_length=MAX_LENGTH, unique=True)
    short_link = models.CharField(max_length=MAX_LENGTH, unique=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=('full_link', 'short_link'), name='recipe_link'
            )
        ]
