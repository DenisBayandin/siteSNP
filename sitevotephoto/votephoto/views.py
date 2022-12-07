from django.contrib.auth import logout, login
from django.contrib.auth.views import LoginView
from django.db.transaction import commit
from django.http import HttpResponse, request, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView

from .forms import *
from .models import User


def main_view(request):
    photos = Photo.objects.all()
    context = {'title': "Главная страница", 'photo': photos}
    return render(request, 'votephoto/main.html', context)


# def addphotoview(request):
#     if request.method == 'POST':
#         form = AddPhotoForm(request.POST, request.FILES)
#         if form.is_valid():
#             form.save()
#             return redirect('main')
#     else:
#         form = AddPhotoForm
#     return render(request, 'votephoto/addphoto.html',{'form': form, 'title':'Добавление фотографии.'})

def profile(request):
    if request.method == 'POST':
        form = AddPhotoForm(request.POST, request.FILES)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.user_id = request.user
            obj.photo_145x165 = get_thumbnailer(obj.oldPhoto)
            obj.photo_510x510 = get_thumbnailer(obj.oldPhoto)
            obj.photo_1680x1680 = get_thumbnailer(obj.oldPhoto)
            obj.save()
            return redirect('main')
    else:
        form = AddPhotoForm
    return render(request, 'votephoto/profile.html', {'form': form, 'title': 'Личный кабинет.'})


def logout_view(request):
    logout(request)
    return redirect('main')


class RegisterUser(CreateView):
    # breakpoint()
    form_class = RegisterUsersForm
    template_name = 'votephoto/register.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Регистрация'
        return context

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('main')


class LoginUser(LoginView):
    form_class = LoginUsersForm
    template_name = 'votephoto/login.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Авторизация'
        return context
