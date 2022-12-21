from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django import forms
import os

from django.core.exceptions import ValidationError
from easy_thumbnails.files import get_thumbnailer

from .models import *
from PIL import Image


class RegisterUsersForm(UserCreationForm):
    username = forms.CharField(label='Имя профиля', widget=forms.TextInput(attrs={'class': 'form-input'}))
    fio = forms.CharField(label='ФИО', widget=forms.TextInput(attrs={'class': 'form-input'}))
    email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'class': 'form-input'}))
    photoUser = forms.ImageField(label='Фото профиля')
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    password2 = forms.CharField(label='Повторить пароль', widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    field_order = ['username', 'fio', 'email', 'photoUser', 'password1', 'password2']

    class Meta:
        model = User
        fields = {'username', 'fio', 'email', 'photoUser', 'password1', 'password2'}


class LoginUsersForm(AuthenticationForm):
    username = forms.CharField(label='Имя профиля', widget=forms.TextInput(attrs={'class': 'form-input'}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-input'}))


class AddPhotoForm(forms.ModelForm):
    namePhoto = forms.CharField(max_length=150, label='Название фотографии',
                                widget=forms.TextInput(attrs={'class': 'form-input'}))
    сontentPhoto = forms.CharField(label='Описание к фотографии', widget=forms.Textarea(attrs={'cols': 80, 'rows': 5}))
    oldPhoto = forms.ImageField(label='Фотография')

    class Meta:
        model = Photo
        fields = ('namePhoto', 'сontentPhoto', 'oldPhoto')

    def clean_oldPhoto(self):
        cleaned_data = super(AddPhotoForm, self).clean()
        file = cleaned_data.get('oldPhoto')
        if file:
            filename = file.name
            if filename.endswith('.jpg'):
                return file
            else:
                raise ValidationError("Вы сохранили файл не с jpg расширением, нам нужно '.jpg'")


class AddComment(forms.ModelForm):
    # contentComment = forms.CharField(label='Комментарий', widget=forms.Textarea(attrs={'cols': 50, 'rows': 5}))

    class Meta:
        model = Comment
        fields = ['contentComment']


# class AddCommentChildren(forms.ModelForm):
#     contentComment = forms.CharField(label='Комментарий', widget=forms.Textarea(attrs={'cols': 50, 'rows': 5}))
#
#     class Meta:
#         model = Comment
#         fields = ['contentComment']
