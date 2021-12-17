from django.http import JsonResponse
from django.shortcuts import render, HttpResponseRedirect, get_object_or_404
from django.template.loader import render_to_string

from basketapp.models import Basket
from mainapp.models import Product
from django.contrib.auth.decorators import login_required


@login_required
def basket(request):
    title = 'корзина'
    baskets_list = Basket.objects.filter(user=request.user). \
        order_by('product__category')

    content = {
        'title': title,
        'basket_items': baskets_list,
    }

    return render(request, 'basketapp/basket.html', content)


@login_required
def add(request, pk):
    product_item = get_object_or_404(Product, pk=pk)

    basket_item = Basket.objects.filter(user=request.user, product=product_item).first()

    if not basket_item:
        basket_item = Basket(user=request.user, product=product_item)

    basket_item.quantity += 1
    basket_item.save()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def remove(request, pk):
    basket_record = get_object_or_404(Basket, pk=pk)
    basket_record.delete()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def basket_edit(request, pk, quantity):
    if request.is_ajax():
        quantity = int(quantity)
        basket_item = Basket.objects.get(pk=pk)

        if quantity > 0:
            basket_item.quantity = quantity
            basket_item.save()
        else:
            basket_item.delete()

        basket_list = Basket.objects.filter(user=request.user)

        context = {
            'basket_items': basket_list,
        }

        result = render_to_string('basketapp/includes/inc_basket_list.html', context)

        return JsonResponse({'result': result})

