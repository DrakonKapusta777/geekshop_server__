import json

from django.conf import settings
from django.contrib.auth.models import User
from authapp.models import ShopUser
from django.core.management.base import BaseCommand

from mainapp.models import ProductCategory, Product

JSON_PATH = 'mainapp/json'


def load_from_json(file_name):
    with open(f"{settings.BASE_DIR}/json/{file_name}.json", 'r', encoding='utf8') as json_file:
        return json.load(json_file)


class Command(BaseCommand):
    def handle(self, *args, **options):
        categories = load_from_json('categories')

        ProductCategory.objects.all().delete()
        for category in categories:
            new_category = ProductCategory(**category)
            new_category.save()

        products = load_from_json('products')

        Product.objects.all().delete()
        for product in products:
            category_name = product["category"]
            _category = ProductCategory.objects.get(name=category_name)
            product['category'] = _category
            new_product = Product(**product)
            new_product.save()

        ShopUser.objects.create_superuser('django', password='geekbrains', age=26)
