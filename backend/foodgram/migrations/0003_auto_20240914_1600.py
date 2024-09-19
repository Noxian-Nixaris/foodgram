# Generated by Django 3.2.3 on 2024-09-14 13:00

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('foodgram', '0002_remove_recipe_score'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='recipe',
            options={'default_related_name': 'recipes', 'ordering': ('name', 'id'), 'verbose_name': 'Рецепт', 'verbose_name_plural': 'Рецепты'},
        ),
        migrations.AlterField(
            model_name='recipe',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='recipes', to=settings.AUTH_USER_MODEL, verbose_name='Автор'),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='ingredient',
            field=models.ManyToManyField(related_name='recipes', through='foodgram.RecipeIngredient', to='foodgram.Ingredient', verbose_name='Ингридиенты'),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='tag',
            field=models.ManyToManyField(related_name='recipes', through='foodgram.RecipeTag', to='foodgram.Tag', verbose_name='Теги'),
        ),
    ]
