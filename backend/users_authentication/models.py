from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    first_name = models.CharField(max_length=150, blank=False)
    last_name = models.CharField(max_length=150, blank=False)
    email = models.EmailField(
        blank=False, max_length=254, verbose_name='email address'
    )
    avatar = models.ImageField(
        upload_to='user_authentication/images/',
        null=True,
        default=None,
        verbose_name='Изображение'
    )
    REQUIRED_FIELDS = ('email', 'first_name', 'last_name')


class UserSubscription(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='subscriptor',
    )
    subscribed = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='subscribed_to',
    )