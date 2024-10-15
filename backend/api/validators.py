from django.core.exceptions import ValidationError


def time_check(cooking_time):
    if cooking_time < 1:
        raise ValidationError()
