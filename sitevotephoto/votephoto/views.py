from django.contrib.auth import logout, login
from django.contrib.auth.views import LoginView
from django.db.transaction import commit
from django.http import HttpResponse, request, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView

from .forms import LoginUsersForm, RegisterUsersForm
from .models import User


def main_view(request):
    # print(request)
    context = {'title': "Главная страница"}
    return render(request, 'votephoto/main.html', context)


def profile(request):
    context = {'title': "Личный кабинет"}
    return render(request, 'votephoto/profile.html', context)


def logout_view(request):
    logout(request)
    return redirect('main')


# def RegisterUser(request):
#     form = RegisterUsersForm
#     # return render(request, 'votephoto/register.html', {'form': form})
#     if request.method == 'POST':
#         form = RegisterUsersForm(request.POST)
#         form.save()
#         return HttpResponseRedirect(reverse('main'))
#     else:
#         return render(request, 'votephoto/register.html', {'form': form})


class RegisterUser(CreateView):
    # breakpoint()
    form_class = RegisterUsersForm
    template_name = 'votephoto/register.html'
    success_url = reverse_lazy('login')

    # def get_context_data(self, *, object_list=None, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['title'] = 'Регистрация'
    #     return context

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
