from django.core.exceptions import ValidationError
from rest_framework import serializers


def positive_check(num):
    if num < 1:
        raise ValidationError(num)


def amount_validation(data):
    if len(data) != len(set(data)) or len(data) == 0:
        raise serializers.ValidationError(data)


def not_empty_validation(data):
    if data is None:
        raise serializers.ValidationError(data)
