from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse

from adminapp.forms import ShopUserAdminEditForm, ProductCategoryEditForm
from authapp.forms import ShopUserRegisterForm
from authapp.models import ShopUser
from mainapp.models import ProductCategory, Product


@user_passes_test(lambda u: u.is_superuser)
def user_create(request):
    title = 'пользователи/создание'

    if request.method == 'POST':
        user_form = ShopUserRegisterForm(request.POST, request.FILES)
        if user_form.is_valid():
            user_form.save()
            return HttpResponseRedirect(reverse('adminapp:user_list'))
    else:
        user_form = ShopUserRegisterForm()

    context = {'title': title, 'form': user_form}

    return render(request, 'adminapp/user_form.html', context)


@user_passes_test(lambda u: u.is_superuser)
def users(request):
    title = 'админка/пользователи'
    users_list = ShopUser.objects.all().order_by('-is_active', '-is_superuser', '-is_staff', 'username')
    context = {
        'title': title,
        'object_list': users_list
    }
    return render(request, 'adminapp/users.html', context)


@user_passes_test(lambda u: u.is_superuser)
def user_update(request, pk):
    title = 'пользователи/редактирование'

    current_user = get_object_or_404(ShopUser, pk=pk)
    if request.method == 'POST':
        user_form = ShopUserAdminEditForm(request.POST, request.FILES, instance=current_user)
        if user_form.is_valid():
            user_form.save()
            return HttpResponseRedirect(reverse('adminapp:user_list'))
    else:
        user_form = ShopUserAdminEditForm(instance=current_user)

    content = {'title': title, 'form': user_form}

    return render(request, 'adminapp/user_form.html', content)


@user_passes_test(lambda u: u.is_superuser)
def user_delete(request, pk):
    title = 'пользователи/удаление'

    current_user = get_object_or_404(ShopUser, pk=pk)

    if request.method == 'POST':
        current_user.is_active = False
        current_user.save()
        return HttpResponseRedirect(reverse('adminapp:user_list'))

    content = {'title': title, 'object': current_user}

    return render(request, 'adminapp/user_delete.html', content)


@user_passes_test(lambda u: u.is_superuser)
def category_create(request):
    title = "категории/создание"

    if request.method == "POST":
        category_form = ProductCategoryEditForm(request.POST, request.FILES)
        if category_form.is_valid():
            category_form.save()
            return HttpResponseRedirect(reverse("adminapp:category_list"))
    else:
        category_form = ProductCategoryEditForm()

    content = {"title": title, "update_form": category_form}

    return render(request, "adminapp/category_update.html", content)


@user_passes_test(lambda u: u.is_superuser)
def categories(request):
    title = 'админка/категории'

    categories_list = ProductCategory.objects.all()

    context = {
        'title': title,
        'object_list': categories_list
    }

    return render(request, 'adminapp/categories.html', context)


@user_passes_test(lambda u: u.is_superuser)
def category_update(request, pk):
    title = "категории/редактирование"

    edit_category = get_object_or_404(ProductCategory, pk=pk)
    if request.method == "POST":
        edit_form = ProductCategoryEditForm(request.POST, request.FILES, instance=edit_category)
        if edit_form.is_valid():
            edit_form.save()
            return HttpResponseRedirect(reverse("adminapp:category_update", args=[edit_category.pk]))
    else:
        edit_form = ProductCategoryEditForm(instance=edit_category)

    content = {"title": title, "update_form": edit_form}

    return render(request, "adminapp/category_update.html", content)


@user_passes_test(lambda u: u.is_superuser)
def category_delete(request, pk):
    title = "категории/удаление"

    category = get_object_or_404(ProductCategory, pk=pk)

    if request.method == "POST":
        category.is_active = False
        category.save()
        return HttpResponseRedirect(reverse("adminapp:category_list"))

    content = {"title": title, "category_to_delete": category}

    return render(request, "adminapp/category_delete.html", content)


@user_passes_test(lambda u: u.is_superuser)
def product_create(request):
    return None


@user_passes_test(lambda u: u.is_superuser)
def products(request, pk):
    title = 'админка/продукт'

    context = {
        'title': title,
        'category': get_object_or_404(ProductCategory, pk=pk),
        'object_list': Product.objects.filter(category__pk=pk).order_by('name'),
    }

    return render(request, 'adminapp/products.html', context)


@user_passes_test(lambda u: u.is_superuser)
def product_detail(request):
    return None


@user_passes_test(lambda u: u.is_superuser)
def product_update(request):
    return None


@user_passes_test(lambda u: u.is_superuser)
def product_delete(request):
    return None
