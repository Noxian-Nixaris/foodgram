# Generated by Django 3.2.3 on 2024-09-06 13:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users_authentication', '0003_user_avatar'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='avatar',
            field=models.ImageField(default=None, null=True, upload_to='user_authentication/images/', verbose_name='Изображение'),
        ),
    ]
