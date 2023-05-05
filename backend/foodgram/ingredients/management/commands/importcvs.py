import csv
import os

from django.conf import settings
from django.core.management.base import BaseCommand
from ingredients.models import Ingredient


def get_reader(file_name):
    csv_path = os.path.join(settings.BASE_DIR, '../../data/', file_name)
    csv_file = open(csv_path, 'r', encoding='utf-8')
    return csv.reader(csv_file, delimiter=',')


class Command(BaseCommand):
    help = 'Импорт ингредиентов из csv-файла'

    def handle(self, *args, **options):
        csv_reader = get_reader('ingredients.csv')
        for row in csv_reader:
            name, measurement_unit = row[0], row[1]
            obj, created = Ingredient.objects.get_or_create(
                name=name, measurement_unit=measurement_unit)
