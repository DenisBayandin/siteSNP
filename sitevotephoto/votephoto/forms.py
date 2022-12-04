from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django import forms

from .models import User


class RegisterUsersForm(UserCreationForm):
    username = forms.CharField(label='Имя профиля', widget=forms.TextInput(attrs={'class': 'form-input'}))
    # fio = forms.CharField(label='ФИО', widget=forms.TextInput(attrs={'class': 'form-input'}))
    email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'class': 'form-input'}))
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    password2 = forms.CharField(label='Повторить пароль', widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    field_order = ['username', 'email', 'password1', 'password2']

    class Meat:
        Meta = UserCreationForm.Meta
        Meta.model = User
        model = User
        fields = {'username', 'email', 'password1', 'password2'}


class LoginUsersForm(AuthenticationForm):
    username = forms.CharField(label='Имя профиля', widget=forms.TextInput(attrs={'class': 'form-input'}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-input'}))
