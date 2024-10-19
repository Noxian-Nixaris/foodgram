# Generated by Django 3.2.3 on 2024-10-17 11:43

import core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('foodgram', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='recipe',
            name='is_favorited',
        ),
        migrations.RemoveField(
            model_name='recipe',
            name='is_in_shopping_cart',
        ),
        migrations.AlterField(
            model_name='recipe',
            name='cooking_time',
            field=models.SmallIntegerField(validators=[core.validators.positive_check, core.validators.max_check], verbose_name='Время приготовления'),
        ),
        migrations.AddConstraint(
            model_name='ingredient',
            constraint=models.UniqueConstraint(fields=('name', 'measurement_unit'), name='name_unit'),
        ),
    ]