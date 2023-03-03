from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import Review, User, Cart


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


class AddToCartForm(forms.ModelForm):
    """ Форма добавления товара в корзину """

    class Meta:
        model = Cart
        fields = ['size', 'quantity']
