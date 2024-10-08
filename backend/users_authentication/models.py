from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models

from core.constants import MAX_EMAIL_LENGTH, MAX_NAME_LENGTH


class User(AbstractUser):
    first_name = models.CharField(max_length=MAX_NAME_LENGTH, blank=False)
    last_name = models.CharField(max_length=MAX_NAME_LENGTH, blank=False)
    email = models.EmailField(
        blank=False,
        max_length=MAX_EMAIL_LENGTH,
        unique=True,
        verbose_name='email address'
    )
    avatar = models.ImageField(
        upload_to='avatars/',
        null=True,
        default=None,
        verbose_name='Изображение'
    )
    REQUIRED_FIELDS = ('username', 'first_name', 'last_name')
    USERNAME_FIELD = 'email'

    class Meta:
        ordering = ('username',)

    def __str__(self):
        return f'{self.username}'


class UserSubscription(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='subscriber',
    )
    subscribed = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='subscribed_to',
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=('user', 'subscribed'), name='subscription'
            )
        ]

    def clean(self):
        if self.user == self.subscribed:
            raise ValidationError('Нельзя подписаться на самого себя')
