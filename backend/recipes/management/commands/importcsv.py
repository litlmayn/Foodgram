import csv
import os

from django.conf import settings
from django.core.management.base import BaseCommand

from recipes.models import Ingredient, Tag


def get_reader(file_name):
    csv_path = os.path.join(settings.BASE_DIR, 'data/', file_name)
    csv_file = open(csv_path, 'r', encoding='utf-8')
    return csv.reader(csv_file, delimiter=',')


class Command(BaseCommand):
    help = 'Импорт ингредиентов из csv-файла'

    def handle(self, *args, **options):
        csv_reader = get_reader('ingredients.csv')
        try:
            for name, measurement_unit in csv_reader:
                Ingredient.objects.get_or_create(
                    name=name, measurement_unit=measurement_unit)
        except FileNotFoundError:
            self.stdout.write(self.style.ERROR(f'Файл {csv_reader} не найден'))
        else:
            self.stdout.write(self.style.SUCCESS('Ингредиенты добавлены.'))

        csv_reader = get_reader('tags.csv')
        try:
            for name, color, slug in csv_reader:
                Tag.objects.get_or_create(
                    name=name, color=color, slug=slug)
        except FileNotFoundError:
            self.stdout.write(self.style.ERROR(f'Файл {csv_reader} не найден'))
        else:
            self.stdout.write(self.style.SUCCESS('Теги добавлены.'))
