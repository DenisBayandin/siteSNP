import json

from django.contrib.auth import logout, login
from django.contrib.auth.views import LoginView
from django.db.models import Count, Q
from django.http import HttpResponse, Http404, HttpResponseBadRequest
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.html import escape
from django.views.generic import CreateView, ListView
from .forms import *


class RegisterUser(CreateView):
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


class MainView(ListView):
    template_name = 'votephoto/main.html'
    context_object_name = 'photo'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Главная страница'
        return context

    def get_queryset(self):
        self.queryset = Photo.objects.all().order_by('-date_create')
        return super().get_queryset()


class MainSortedView(ListView):
    template_name = 'votephoto/sortedMain.html'
    context_object_name = 'photo'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Отсортированная главная страница'
        return context

    def get_queryset(self):
        get_sorted_name = self.kwargs.get('sorting')
        self.queryset = Photo.objects.all().order_by(get_sorted_name)
        return super().get_queryset()


class MainSearchView(ListView):
    template_name = 'votephoto/searchMain.html'
    context_object_name = 'photo'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Поиск'
        return context

    def get_queryset(self):
        what_wrote_to_user = self.kwargs.get('search')
        self.queryset = Photo.objects.filter(
            Q(name__icontains=what_wrote_to_user) | Q(content__icontains=what_wrote_to_user))
        if self.queryset.count() == 0:
            photo_search = []
            user_search = User.objects.filter(username__icontains=what_wrote_to_user)
            if user_search != 0:
                for user_in_search in user_search:
                    user_photo = Photo.objects.filter(user=user_in_search.pk)
                    for photo_one in user_photo:
                        photo_search.append(photo_one)
                self.queryset = photo_search
            else:
                self.queryset = None
        elif User.objects.filter(username__icontains=what_wrote_to_user) != 0:
            photo_search_to_user = []
            user_search = User.objects.filter(username__icontains=what_wrote_to_user)
            for user_in_search in user_search:
                all_photo_to_one_user = Photo.objects.filter(user=user_in_search.pk)
                for one_photo_to_one_user in all_photo_to_one_user:
                    photo_search_to_user.append(one_photo_to_one_user)
            set_gueryset = set(self.queryset)
            set_photo_search_to_user = set(photo_search_to_user)
            self.queryset = list(set_gueryset.union(set_photo_search_to_user))
        else:
            self.queryset = None
        return super().get_queryset()


# def searchView(request):
#     query = request.GET.get('q')
#     objects = Photo.objects.filter(Q(name__icontains=query) | Q(content__icontains=query))
#     context = {'title': 'Поиск', 'objects': objects}
#     return render(request, 'votephoto/search.html', context)


def showOnePhoto(request, photoID):
    comment_show = Comment.objects.filter(photo=photoID, Parent=None)
    commentChildren_show = Comment.objects.exclude(Parent=None).filter(photo=photoID)
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
            obj.user = request.user
            obj.photo = photo
            obj.save()
            add_comment_to_photo = Photo.objects.get(pk=photoID)
            add_comment_to_photo.count_comment += 1
            add_comment_to_photo.save()
            return redirect(photo.get_absolute_url())
    else:
        form = AddComment
    return render(request, 'votephoto/showOnePhoto.html',
                  {'form': form,
                   'photo': photo,
                   'title': photo.name,
                   'show_comments': comment_show,
                   'show_children_comment': commentChildren_show})


def delete_photo(request, photoID):
    photo = get_object_or_404(Photo, pk=photoID)
    photo.delete()
    return redirect('all_photo')


def update_photo(photoID):
    up_photo = get_object_or_404(Photo, pk=photoID)
    up_photo.old_photo = up_photo.new_photo
    up_photo.new_photo = None
    up_photo.save()


def loading_new_photo(request, photoID):
    photo = get_object_or_404(Photo, pk=photoID)
    if request.method == 'POST':
        form = AddNewPhotoForm(request.POST, request.FILES)
        if form.is_valid():
            obj = form.save(commit=False)
            if form.data['new_photo'] == '':
                photo.name = obj.name
                photo.content = obj.content
                photo.save()
                return redirect('all_photo')
            else:
                photo.name = obj.name
                photo.content = obj.content
                photo.new_photo = obj.new_photo
                photo.save()
                update_photo(photoID)
                return redirect('all_photo')
    else:
        form = AddNewPhotoForm
    context = {'title': f'Обновление фотографии - {photo.name}', 'form': form, 'photo': photo}
    return render(request, 'votephoto/loadingNewPhoto.html', context)


def delete_comment(request, commentID, photoID):
    comment = get_object_or_404(Comment, pk=commentID)
    comment_children_all = Comment.objects.filter(Parent=commentID)
    for comment_children in comment_children_all:
        if comment_children.Parent.pk == comment.pk:
            raise ValidationError("Невозможно удалить данный комментарий.")
    if request.user == comment.user:
        comment.delete()
        remove_comment_to_photo = Photo.objects.get(pk=photoID)
        remove_comment_to_photo.count_comment -= 1
        remove_comment_to_photo.save()
        return redirect('show_photo', photoID)


def update_comment(request, commentID, photoID):
    comment = get_object_or_404(Comment, pk=commentID)
    if request.user == comment.user:
        val_comment = 'newComment' + str(commentID)
        if request.POST[val_comment] is not None:
            newContent = request.POST[val_comment]
            comment.content = newContent
            comment.save()
            return redirect('show_photo', photoID)
        else:
            return HttpResponse("13321313132231")


# def sortedPhoto(request, need_sort):
#     photos = []
#     if need_sort == 'DUP':
#         photos = Photo.objects.all().order_by('date_update')
#     elif need_sort == 'DDOWN':
#         photos = Photo.objects.all().order_by('-date_update')
#     elif need_sort == 'CDOWN':
#         comment_sorted = Comment.objects.values('photo').annotate(count_comment=Count('pk')).order_by(
#             '-count_comment')
#         for photo in comment_sorted:
#             photos.append(Photo.objects.get(pk=photo['photo']))
#     elif need_sort == 'CUP':
#         comment_sorted = Comment.objects.values('photo').annotate(count_comment=Count('pk')).order_by(
#             'count_comment')
#         for photo in comment_sorted:
#             photos.append(Photo.objects.get(pk=photo['photo']))
#         # return HttpResponse(status=200)
#     elif need_sort == 'LUP':
#         like_sorted = Like.objects.values('photo').annotate(count_like=Count('pk')).order_by('count_like')
#         for photo in like_sorted:
#             photos.append(Photo.objects.get(pk=photo['photo']))
#     elif need_sort == 'LDOWN':
#         like_sorted = Like.objects.values('photo').annotate(count_like=Count('pk')).order_by('-count_like')
#         for photo in like_sorted:
#             photos.append(Photo.objects.get(pk=photo['photo']))
#     return photos


# def main_view(request):
#     photos = sortedPhoto(request)
#     sort_form = SortedForm
#     context = {'title': "Главная страница",
#                'photo': photos,
#                'sort_form': sort_form}
#     return render(request, 'votephoto/main.html', context)


def profile(request):
    if request.method == 'POST':
        form = AddPhotoForm(request.POST, request.FILES)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.user = request.user
            obj.save()
            return redirect('main')
    else:
        form = AddPhotoForm
    return render(request, 'votephoto/profile.html', {'form': form, 'title': 'Личный кабинет'})


def logout_view(request):
    logout(request)
    return redirect('main')


def addlike(request):
    if request.user.is_authenticated:
        is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
        data = json.load(request)
        photoID = data.get('photoID')
        if is_ajax:
            if request.method == 'POST':
                if Like.objects.filter(photo=photoID, user=request.user).exists():
                    one_like_user = Like.objects.get(photo=photoID, user=request.user)
                    one_like_user.delete()
                    remove_like_to_photo = Photo.objects.get(pk=photoID)
                    remove_like_to_photo.count_like -= 1
                    remove_like_to_photo.save()
                    return HttpResponse(status=200)
                else:
                    photo = get_object_or_404(Photo, pk=photoID)
                    like = Like()
                    like.user = request.user
                    like.photo = photo
                    like.save()
                    add_like_to_photo = Photo.objects.get(pk=photoID)
                    add_like_to_photo.count_like += 1
                    add_like_to_photo.save()
                    return HttpResponse(status=201)
        else:
            return HttpResponse("Ошибка.", status=400, reason='Invalid request')
    else:
        return HttpResponse(status=202)


def viewAllPhoto(request):
    photos = Photo.objects.filter(user=request.user)
    # breakpoint()
    context = {'title': f'Фотографии {request.user.username}-a', 'photo': photos}
    return render(request, 'votephoto/allPhotoOneUser.html', context)
