# Generated by Django 3.2.3 on 2024-09-15 13:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('foodgram', '0003_auto_20240914_1600'),
    ]

    operations = [
        migrations.RenameField(
            model_name='recipe',
            old_name='ingredient',
            new_name='ingredients',
        ),
        migrations.RenameField(
            model_name='recipe',
            old_name='tag',
            new_name='tags',
        ),
        migrations.DeleteModel(
            name='UserSubscribe',
        ),
    ]
