from django.core.exceptions import ValidationError


def positive_check(num):
    if num < 1:
        raise ValidationError()


