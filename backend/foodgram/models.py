from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser

User = get_user_model()


# class User(AbstractUser):
#     pass


class Tag(models.Model):
    name = models.CharField(
        max_length=256,
        unique=True,
        verbose_name='Название'
    )
    slug = models.SlugField(unique=True, verbose_name='Слаг')

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    name = models.CharField(
        max_length=256,
        unique=True,
        verbose_name='Название'
    )
    measurement_unit = models.CharField(
        max_length=256,
        verbose_name='Единица измерения'
    )

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'
        ordering = ('name', 'id')

    def __str__(self):
        return self.name


class Recipe(models.Model):
    name = models.CharField(max_length=256, verbose_name='Название')
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор'
    )
    image = models.ImageField(
        upload_to='foodgram/images/',
        null=True,
        default=None,
        verbose_name='Изображение'
    )
    text = models.TextField(verbose_name='Описание')
    ingredient = models.ManyToManyField(
        Ingredient,
        through='RecipeIngredient',
        verbose_name='Ингридиенты'
    )
    tag = models.ManyToManyField(Tag, through='RecipeTag', verbose_name='Теги')
    cooking_time = models.SmallIntegerField(verbose_name='Время приготовления')
    score = models.SmallIntegerField(verbose_name='В избранном')

    class Meta:
        default_related_name = 'recipe'
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'
        ordering = ('name', 'id')

    def __str__(self):
        return self.name[:50]


class UserSubscribe(models.Model):
    name = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Пользователь'
    )
    subscribed_to = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name='Подписан на'
    )

    class Meta:
        ordering = ('name', 'subscribed_to')
        default_related_name = 'subscription'
        constraints = [
            models.UniqueConstraint(
                fields=('name', 'subscribed_to'), name='user_subscription'
            )
        ]


class RecipeTag(models.Model):
    recepe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.recepe} {self.tag}'


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    amount = models.IntegerField(verbose_name='Количество')

    def __str__(self):
        return f'{self.recepe} {self.ingredient}'
