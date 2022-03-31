from django.core.management.base import BaseCommand
from csv import DictReader
from products.models import Product


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('file_name', type=str)

    def handle(self, *args, **options):
        file = options['file_name']
        with open(file, 'r') as f:
            csv_reader = DictReader(f)
            for row in csv_reader:
                name = row['name']
                price = row['price']
                present = row['present']
                description = row['description']
                Product.objects.create(name=name, price=price, present=present, description=description)
        print(f'Products are created from: {file}')
