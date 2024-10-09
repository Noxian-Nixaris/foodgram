import json

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.db.utils import IntegrityError

from foodgram.models import Ingredient, Tag

User = get_user_model()


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument("json_to_db")

    def handle(self, *args, **options):
        try:
            with open('data/ingredients.json', 'r') as file:
                data = json.load(file)
                instance = (Ingredient(**ingr) for ingr in data)
                Ingredient.objects.bulk_create(instance)
        except IntegrityError:
            pass
        try:
            with open('data/tags.json', 'r') as file_tag:
                data = json.load(file_tag)
                instance = (Tag(**d) for d in data)
                Tag.objects.bulk_create(instance)
        except IntegrityError:
            pass
