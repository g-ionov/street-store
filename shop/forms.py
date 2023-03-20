from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from phonenumber_field.formfields import PhoneNumberField

from .models import Review, User, Cart, Order, Coupon


class ReviewForm(forms.ModelForm):
    """ Форма отзыва """
    order = forms.ChoiceField(required=True)

    class Meta:
        model = Review
        fields = ['model', 'grade', 'text', 'order']


class CustomUserCreationForm(UserCreationForm):
    """ Форма создания нового пользователя"""

    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('phone', 'email', 'first_name', 'last_name', 'birth_date')


class UserEditForm(forms.Form):
    """ Форма редактирования пользователя """

    first_name = forms.CharField(required=False)
    last_name = forms.CharField(required=False)
    email = forms.EmailField(required=False)
    phone = PhoneNumberField(required=False)
    birth_date = forms.DateField(required=False)


class AddToCartForm(forms.ModelForm):
    """ Форма добавления товара в корзину """
    quantity = forms.IntegerField(required=False)

    class Meta:
        model = Cart
        fields = ['size', 'quantity']


class CheckoutForm(forms.Form):
    """ Форма оформления заказа """
    first_name = forms.CharField(max_length=64, required=False, label='Имя')
    last_name = forms.CharField(max_length=64, required=False, label='Фамилия')
    phone = PhoneNumberField(required=False, label='Телефон')
    city = forms.CharField(max_length=25, label='Город')
    street = forms.CharField(max_length=32, label='Улица')
    number = forms.CharField(max_length=4, label='Дом')
    block = forms.CharField(max_length=3, required=False, label='Корпус')
    apartment = forms.CharField(max_length=6, required=False, label='Квартира')
    zip_code = forms.CharField(max_length=6, label='Индекс')
    coupon = forms.CharField(max_length=50, required=False, label='Купон')


class CouponForm(forms.Form):
    """ Форма для ввода купона"""
    code = forms.CharField(max_length=50)


class DatePeriodForm(forms.Form):
    """ Форма для ввода периода дат"""
    start_date = forms.DateField(required=False)
    end_date = forms.DateField(required=False)
    all_time = forms.BooleanField(required=False)
