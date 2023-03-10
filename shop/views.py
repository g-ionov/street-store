from django.contrib import messages
from django.contrib.auth import login
from django.shortcuts import render, redirect
from django.views.generic import DetailView, ListView
from django.views.generic.base import View
from django.http import HttpResponseRedirect

from .forms import ReviewForm, CustomUserCreationForm, AddToCartForm, UserEditForm
from .models import Model, Review, User
from .services import add_to_wishlist, remove_from_wishlist, is_model_in_wishlist, get_new_models, \
    get_best_selling_products, get_brands, get_model, get_model_sizes_quantity_in_stock, \
    create_or_update_review, remove_from_cart, add_to_cart, delete_user, edit_user, delete_review


class ModelDetailView(DetailView):
    """ Полное описание товара """
    model = Model
    template_name = 'shop/model_detail.html'
    slug_field = 'url'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['review_form'] = ReviewForm()
        return context


class AddReview(View):
    """ Добавить новый отзыв """

    def post(self, request, *args, **kwargs):
        if kwargs['action'] == 'add':
            create_or_update_review(request.user, request.POST['model'], request.POST['order'],
                                    request.POST['grade'], request.POST['text'])
            messages.success(request, 'Ваш отзыв успешно добавлен')
        elif kwargs['action'] == 'delete':
            delete_review(request.POST['review'])
            messages.success(request, 'Ваш отзыв успешно удален')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


class UserView(View):
    """ Личный кабинет пользователя """

    def get(self, request, *args, **kwargs):
        if request.GET.get('action') == 'edit':
            return render(request, 'shop/edit_user.html', {})
        return render(request, 'shop/user.html', {}) if request.user.is_authenticated else redirect('login')

    def post(self, request, *args, **kwargs):
        if request.POST['action'] == 'delete':
            delete_user(request.user)
            messages.success(request, 'Ваш аккаунт успешно удален')
            return redirect('index')
        elif request.POST['action'] == 'edit':
            form = UserEditForm(request.POST)
            print(form.errors)
            if form.is_valid():
                edit_user(request.user, form.cleaned_data),
                return redirect('me')
            else:
                return render(request, 'shop/edit_user.html', {'form_errors': form.errors})
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


class MainView(View):
    """ Главная страница """

    def get(self, request, *args, **kwargs):
        return render(request, 'shop/home.html',
                      {'man_new_models': get_new_models('M'),
                       'women_new_models': get_new_models('F'),
                       'man_best_selling_products': get_best_selling_products('M'),
                       'women_best_selling_products': get_best_selling_products('F'),
                       'brands': get_brands()})


class RegisterUserView(View):
    """ Регистрация нового пользователя"""

    def post(self, request, *args, **kwargs):
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index')
        return render(request, "registration/register.html", context={"register_form": form})

    def get(self, request, *args, **kwargs):
        form = CustomUserCreationForm()
        return render(request, "registration/register.html", context={"register_form": form})


class CartView(View):
    """ Корзина """

    def get(self, request, *args, **kwargs):
        return render(request, 'shop/cart.html', {})

    def post(self, request, pk, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        if request.POST['action'] == 'add':
            form = AddToCartForm(request.POST)
            if form.is_valid():
                if not form.cleaned_data['quantity']:
                    form.quantity = 1
                if get_model_sizes_quantity_in_stock(pk, form.cleaned_data['size']) < \
                        form.cleaned_data['quantity']:
                    messages.error(request, 'Недостаточно товара на складе')
                else:
                    add_to_cart(request.user, pk, form.cleaned_data['size'], form.cleaned_data['quantity'])
                    messages.success(request, 'Товар успешно добавлен в корзину')
        elif request.POST['action'] == 'remove':
            remove_from_cart(request.user, pk)
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


class WishlistView(View):
    """ Список желаемых товаров """

    def get(self, request, *args, **kwargs):
        return render(request, 'shop/wishlist.html', {})

    def post(self, request, *args, **kwargs):
        model = get_model(kwargs['pk'])
        user = request.user
        if user.is_authenticated:
            if is_model_in_wishlist(user, model):
                remove_from_wishlist(user, model)
                messages.success(request, 'Товар успешно удален из списка желаемых товаров')
            else:
                add_to_wishlist(user, model)
                messages.success(request, 'Товар успешно добавлен в список желаемых товаров')
        else:
            return redirect('login')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
