import random

from django.shortcuts import render, get_object_or_404

from basketapp.models import Basket
from mainapp.models import Product, ProductCategory


def index(request):
    context = {
        'title': 'Главная',
        'products': Product.objects.all()[:4],
        'basket': get_basket(request.user)
    }
    return render(request, "mainapp/index.html", context)


def contact(request):
    context = {
        'title': 'Контакты',
        'basket': get_basket(request.user)
    }
    return render(request, "mainapp/contact.html", context)


def get_basket(user):
    if user.is_authenticated:
        return Basket.objects.filter(user=user)
    return[]


def get_hot_product():
    return random.sample(list(Product.objects.all()), 1)[0]


def get_same_product(hot_product):
    product_list = Product.objects.filter(category=hot_product.category).exclude(pk=hot_product.pk)[:3]
    return product_list


def products(request, pk=None):
    title = 'продукты'
    links_menu = ProductCategory.objects.all()

    if pk is not None:
        if pk == 0:
            products = Product.objects.all().order_by('price')
            category = {'name': 'все'}
        else:
            category = get_object_or_404(ProductCategory, pk=pk)
            products = Product.objects.filter(category__pk=pk).order_by('price')

        context = {
            'title': title,
            'links_menu': links_menu,
            'category': category,
            'products': products,
            'basket': get_basket(request.user)
        }

        return render(request, 'mainapp/products_list.html', context)

    hot_product = get_hot_product()
    same_products = get_same_product(hot_product)

    context = {
        'title': title,
        'links_menu': links_menu,
        'hot_product': hot_product,
        'same_products': same_products,
        'basket': get_basket(request.user)
    }

    return render(request, 'mainapp/products.html', context)


def product(request, pk):
    title = 'продукты'

    content = {
        'title': title,
        'links_menu': ProductCategory.objects.all(),
        'product': get_object_or_404(Product, pk=pk),
        'basket': get_basket(request.user),
    }

    return render(request, 'mainapp/product.html', content)


