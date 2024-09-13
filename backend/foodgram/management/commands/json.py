import json

from django.core.management.base import BaseCommand

from foodgram.models import Ingredient

STATIC_PASS = '../data/'


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument("json_to_db")

    def handle(self, *args, **options):
        with open(
            f'{STATIC_PASS}ingredients.json', 'r'
        ) as file:
            data = json.load(file)
            for ingr in data:
                Ingredient.objects.get_or_create(
                    name=ingr['name'],
                    measurement_unit=ingr['measurement_unit']
                )
