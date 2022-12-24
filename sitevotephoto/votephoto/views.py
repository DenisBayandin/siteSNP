import json

from django.contrib.auth import logout, login
from django.contrib.auth.views import LoginView
from django.db.transaction import commit
from django.http import HttpResponse, request, HttpResponseRedirect, Http404, JsonResponse, HttpResponseBadRequest
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView
from .forms import *


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


def showOnePhoto(request, photoID):
    comment_show = Comment.objects.filter(photo_id=photoID, Parent=None)
    commentChildren_show = Comment.objects.exclude(Parent=None).filter(photo_id=photoID)
    try:
        photo = get_object_or_404(Photo, pk=photoID)
    except:
        raise Http404(f'Фотографии {photoID} не существует')
    # if request.user.is_authenticated:
    if request.method == "POST":
        form = AddComment(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            if request.POST.get("answer", None):
                id = int(request.POST.get("answer"))
                obj.Parent = Comment.objects.get(pk=id)
            # else:
            #     raise Http404()
            obj.user_id = request.user
            obj.photo_id = photo
            obj.save()
            return redirect(photo.get_absolute_url())
    else:
        form = AddComment
    return render(request, 'votephoto/showOnePhoto.html',
                  {'form': form, 'photo': photo, 'title': photo.namePhoto, 'show_comments': comment_show,
                   'show_children_comment': commentChildren_show})


def main_view(request):
    photos = Photo.objects.all()
    context = {'title': "Главная страница", 'photo': photos}
    return render(request, 'votephoto/main.html', context)


def profile(request):
    if request.method == 'POST':
        form = AddPhotoForm(request.POST, request.FILES)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.user_id = request.user
            obj.save()
            return redirect('main')
    else:
        form = AddPhotoForm
    return render(request, 'votephoto/profile.html', {'form': form, 'title': 'Личный кабинет.'})


def logout_view(request):
    logout(request)
    return redirect('main')


# def addlike(request, photoID):
#     if request.user.is_authenticated:
#         like = Like.objects.filter(user_id=request.user)
#         photo = get_object_or_404(Photo, pk=photoID)
#         if request.method == 'POST' and request.is_ajax():
#             if Like.objects.filter(photo_id=photoID, user_id=request.user).exists():
#                 one_like_user = Like.objects.get(photo_id=photoID, user_id=request.user)
#                 one_like_user.delete()
#                 # return redirect('main')
#                 return JsonResponse({'countlikes': Like.objects.filter(photo_id=photo.photoID).count()})
#             else:
#                 like = Like()
#                 like.user_id = request.user
#                 like.photo_id = photo
#                 like.save()
#                 return JsonResponse({'countlikes': Like.objects.filter(photo_id=photo.photoID).count()})
#                 # return redirect('main')
#     else:
#         return redirect('login')

def addlike(request):
    if request.user.is_authenticated:
        is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
        data = json.load(request)
        photoID = data.get('photoID')
        if is_ajax:
            if request.method == 'POST':
                if Like.objects.filter(photo_id=photoID, user_id=request.user).exists():
                    one_like_user = Like.objects.get(photo_id=photoID, user_id=request.user)
                    one_like_user.delete()
                    return HttpResponse(status=200)
                else:
                    photo = get_object_or_404(Photo, pk=photoID)
                    like = Like()
                    like.user_id = request.user
                    like.photo_id = photo
                    like.save()
                    return HttpResponse(status=201)
        else:
            return HttpResponseBadRequest('Invalid request')
    else:
        return HttpResponse(status=202)