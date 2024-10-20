from django.core.exceptions import ValidationError
from rest_framework import serializers


def positive_check(num):
    if num < 1:
        raise ValidationError('Числоо должно быть больше 0')


def max_check(num):
    if num > 999:
        raise ValidationError(num)


def not_empty_validation(data):
    if data is None:
        raise serializers.ValidationError(data)
