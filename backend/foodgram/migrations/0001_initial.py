# Generated by Django 3.2.3 on 2024-08-30 13:36

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Ingredient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256, unique=True, verbose_name='Название')),
                ('measurement_unit', models.CharField(max_length=256, verbose_name='Единица измерения')),
            ],
            options={
                'verbose_name': 'Ингредиент',
                'verbose_name_plural': 'Ингредиенты',
                'ordering': ('name', 'id'),
            },
        ),
        migrations.CreateModel(
            name='Recipe',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256, verbose_name='Название')),
                ('image', models.ImageField(default=None, null=True, upload_to='foodgram/images/', verbose_name='Изображение')),
                ('text', models.TextField(verbose_name='Описание')),
                ('cooking_time', models.SmallIntegerField(verbose_name='Время приготовления')),
                ('score', models.SmallIntegerField(verbose_name='В избранном')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='recipe', to=settings.AUTH_USER_MODEL, verbose_name='Автор')),
            ],
            options={
                'verbose_name': 'Рецепт',
                'verbose_name_plural': 'Рецепты',
                'ordering': ('name', 'id'),
                'default_related_name': 'recipe',
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256, unique=True, verbose_name='Название')),
                ('slug', models.SlugField(unique=True, verbose_name='Слаг')),
            ],
        ),
        migrations.CreateModel(
            name='UserSubscribe',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subscription', to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
                ('subscribed_to', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subscription', to='foodgram.recipe', verbose_name='Подписан на')),
            ],
            options={
                'ordering': ('name', 'subscribed_to'),
                'default_related_name': 'subscription',
            },
        ),
        migrations.CreateModel(
            name='RecipeTag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('recepe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='foodgram.recipe')),
                ('tag', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='foodgram.tag')),
            ],
        ),
        migrations.CreateModel(
            name='RecipeIngredient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.IntegerField(verbose_name='Количество')),
                ('ingredient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='foodgram.ingredient')),
                ('recipe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='foodgram.recipe')),
            ],
        ),
        migrations.AddField(
            model_name='recipe',
            name='ingredient',
            field=models.ManyToManyField(related_name='recipe', through='foodgram.RecipeIngredient', to='foodgram.Ingredient', verbose_name='Ингридиенты'),
        ),
        migrations.AddField(
            model_name='recipe',
            name='tag',
            field=models.ManyToManyField(related_name='recipe', through='foodgram.RecipeTag', to='foodgram.Tag', verbose_name='Теги'),
        ),
        migrations.AddConstraint(
            model_name='usersubscribe',
            constraint=models.UniqueConstraint(fields=('name', 'subscribed_to'), name='user_subscription'),
        ),
    ]