from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView

from adminapp.forms import ShopUserAdminEditForm, ProductCategoryEditForm, ProductEditForm
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


# @user_passes_test(lambda u: u.is_superuser)
# def users(request):
#    title = 'админка/пользователи'
#    users_list = ShopUser.objects.all().order_by('-is_active', '-is_superuser', '-is_staff', 'username')
#    context = {
#        'title': title,
#        'object_list': users_list
#    }
#    return render(request, 'adminapp/users.html', context)


class UsersListView(ListView):
    model = ShopUser
    template_name = 'adminapp/users.html'

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


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


# @user_passes_test(lambda u: u.is_superuser)
# def product_create(request):
#     return None

class ProductCreateView(CreateView):
    model = Product
    template_name = 'adminapp/product_form.html'
    form_class = ProductEditForm

    def get_success_url(self):
        return reverse('adminapp:product_list', args=[self.kwargs['pk']])


# @user_passes_test(lambda u: u.is_superuser)
# def products(request, pk):
#     title = 'админка/продукт'
#
#     context = {
#         'title': title,
#         'category': get_object_or_404(ProductCategory, pk=pk),
#         'object_list': Product.objects.filter(category__pk=pk).order_by('name'),
#     }
#
#     return render(request, 'adminapp/products.html', context)

class ProductListView(ListView):
    model = Product
    template_name = 'adminapp/products.html'

    def get_context_data(self, *args, **kwargs):
        context_data = super().get_context_data(*args, **kwargs)
        context_data['category'] = get_object_or_404(ProductCategory, pk=self.kwargs.get('pk'))
        return context_data

    def get_queryset(self):
        return Product.objects.filter(category__pk=self.kwargs.get('pk'))


# @user_passes_test(lambda u: u.is_superuser)
# def product_detail(request):
#     return None

class ProductDetailView(DetailView):
    model = Product
    template_name = 'adminapp/product_detail.html'


# @user_passes_test(lambda u: u.is_superuser)
# def product_update(request):
#     return None

class ProductUpdateView(UpdateView):
    model = Product
    template_name = 'adminapp/product_form.html'
    form_class = ProductEditForm

    def get_success_url(self):
        product_item = Product.objects.get(pk=self.kwargs['pk'])
        return reverse('adminapp:product_list', args=[product_item.category_id])


# @user_passes_test(lambda u: u.is_superuser)
# def product_delete(request):
#     return None


class ProductDeleteView(DeleteView):
    model = Product
    template_name = 'adminapp/product_delete.html'

    def get_success_url(self):
        product_item = Product.objects.get(pk=self.kwargs['pk'])
        return reverse('adminapp:product_list', args=[product_item.category_id])

    # def delete(self, request, *args, **kwargs):
    #     if self.object.is_active:
    #         self.object.is_active = False
    #     else:
    #         self.object.is_active = True
    #     self.object.save()
    #     return HttpResponseRedirect(reverse('adminapp:product_list', args=[self.object.category_id]))

