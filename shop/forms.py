from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from phonenumber_field.formfields import PhoneNumberField

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


class UserEditForm(forms.Form):
    """ Форма редактирования пользователя """
    
    first_name = forms.CharField(required=False)
    last_name = forms.CharField(required=False)
    email = forms.EmailField(required=False)
    phone = PhoneNumberField(required=False)
    birth_date = forms.DateField(required=False)


class AddToCartForm(forms.ModelForm):
    """ Форма добавления товара в корзину """

    class Meta:
        model = Cart
        fields = ['size', 'quantity']
