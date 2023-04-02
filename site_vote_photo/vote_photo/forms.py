from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.exceptions import ValidationError

from .models import User, Photo, Comment


class RegisterUsersForm(UserCreationForm):
    username = forms.CharField(
        label="Имя профиля", widget=forms.TextInput(attrs={"class": "form-input"})
    )
    first_name = forms.CharField(
        label="Имя", widget=forms.TextInput(attrs={"class": "form-input"})
    )
    last_name = forms.CharField(
        label="Фамилия", widget=forms.TextInput(attrs={"class": "form-input"})
    )
    patronymic = forms.CharField(
        label="Отчество", widget=forms.TextInput(attrs={"class": "form-input"})
    )
    email = forms.EmailField(
        label="Email", widget=forms.EmailInput(attrs={"class": "form-input"})
    )
    photo_by_user = forms.ImageField(label="Фото профиля")
    password1 = forms.CharField(
        label="Пароль", widget=forms.PasswordInput(attrs={"class": "form-input"})
    )
    password2 = forms.CharField(
        label="Повторить пароль",
        widget=forms.PasswordInput(attrs={"class": "form-input"}),
    )
    field_order = [
        "username",
        "last_name",
        "first_name",
        "patronymic",
        "email",
        "photo_by_user",
        "password1",
        "password2",
    ]

    class Meta:
        model = User
        fields = {
            "username",
            "first_name",
            "last_name",
            "patronymic",
            "email",
            "photo_by_user",
            "password1",
            "password2",
        }


class LoginUsersForm(AuthenticationForm):
    username = forms.CharField(
        label="Имя профиля", widget=forms.TextInput(attrs={"class": "form-input"})
    )
    password = forms.CharField(
        label="Пароль", widget=forms.PasswordInput(attrs={"class": "form-input"})
    )


class AddPhotoForm(forms.ModelForm):
    name = forms.CharField(
        max_length=150,
        label="Название фотографии",
        widget=forms.TextInput(attrs={"class": "form-input"}),
    )
    content = forms.CharField(
        label="Описание к фотографии",
        widget=forms.Textarea(attrs={"cols": 80, "rows": 5}),
    )
    old_photo = forms.ImageField(label="Фотография")

    class Meta:
        model = Photo
        fields = ("name", "content", "old_photo")

    def clean_oldPhoto(self):
        cleaned_data = super(AddPhotoForm, self).clean()
        file = cleaned_data.get("oldPhoto")
        if file:
            filename = file.name
            if filename.endswith(".jpg"):
                return file
            else:
                raise ValidationError(
                    "Вы сохранили файл не с jpg расширением," " нам нужно '.jpg'"
                )


class AddComment(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["content"]


class AddNewPhotoForm(forms.ModelForm):
    name = forms.CharField(
        max_length=150,
        label="Название фотографии",
        widget=forms.TextInput(attrs={"class": "form-input"}),
    )
    content = forms.CharField(
        label="Описание к фотографии",
        widget=forms.Textarea(attrs={"cols": 80, "rows": 5}),
    )
    new_photo = forms.ImageField(label="Новая фотография", required=True)

    class Meta:
        model = Photo
        fields = ("name", "content", "new_photo")

    def clean_oldPhoto(self):
        cleaned_data = super(AddNewPhotoForm, self).clean()
        file = cleaned_data.get("new_photo")
        if file:
            filename = file.name
            if filename.endswith(".jpg"):
                return file
            else:
                raise ValidationError(
                    "Вы сохранили файл не с jpg расширением," " нам нужно '.jpg'"
                )

    def __init__(self, *args, **kwargs):
        super(AddNewPhotoForm, self).__init__(*args, **kwargs)

        for key in self.fields:
            self.fields["name"].required = False
            self.fields["content"].required = False
            self.fields["new_photo"].required = False


class UpdatePasswordForm(forms.Form):
    password = forms.CharField(
        label="Ваш пароль", widget=forms.TextInput(attrs={"class": "form-input"})
    )
    new_password = forms.CharField(
        label="Новый пароль", widget=forms.TextInput(attrs={"class": "form-input"})
    )
    new_password2 = forms.CharField(
        label="Повторите пароль", widget=forms.TextInput(attrs={"class": "form-input"})
    )
