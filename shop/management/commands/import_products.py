import yaml
from django.core.management.base import BaseCommand
from shop.models import Category, Product, Supplier
import os

class Command(BaseCommand):
    help = 'Import products from a specified YAML file in uploads directory'

    def add_arguments(self, parser):
        parser.add_argument('filename', type=str, help='The filename of the YAML file to import')

    def handle(self, *args, **kwargs):
        filename = kwargs['filename']
        filepath = os.path.join('uploads', filename)
        if not os.path.exists(filepath):
            self.stdout.write(self.style.ERROR(f'File {filename} does not exist in uploads directory'))
            return

        self.import_products_from_file(filepath)

    def import_products_from_file(self, filepath):
        with open(filepath, 'r') as file:
            data = yaml.safe_load(file)

            supplier_name = data['shop']
            supplier, created = Supplier.objects.get_or_create(name=supplier_name)

            for category_data in data.get('categories', []):
                category, created = Category.objects.get_or_create(
                    id=category_data['id'], defaults={'name': category_data['name']}
                )

            for product_data in data.get('goods', []):
                category = Category.objects.get(id=product_data['category'])
                product, created = Product.objects.get_or_create(
                    id=product_data['id'],
                    defaults={
                        'category': category,
                        'supplier': supplier,
                        'model': product_data['model'],
                        'name': product_data['name'],
                        'price': product_data['price'],
                        'price_rrc': product_data['price_rrc'],
                        'quantity': product_data['quantity'],
                        'parameters': product_data['parameters'],
                    }
                )
        self.stdout.write(self.style.SUCCESS(f'Successfully imported products from {os.path.basename(filepath)}'))
