import json
from django.utils import timezone
from datetime import datetime, timedelta
from celery import shared_task
from django.contrib.auth import logout, login
from django.contrib.auth.views import LoginView
from django.db.models import Count, Q
from django.http import HttpResponse, Http404, HttpResponseBadRequest
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.views.generic import CreateView, ListView
from .forms import *
from django_celery_beat.models import PeriodicTask, IntervalSchedule


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
        self.queryset = Photo.objects.filter(state='Verified')
        return super().get_queryset()


class MainSortedView(ListView):
    template_name = 'votephoto/sortedMain.html'
    context_object_name = 'photo'

    def get_queryset(self):
        get_sorted_name = self.kwargs.get('sorting')
        self.queryset = Photo.objects.filter(state='Verified').order_by(get_sorted_name)
        return super().get_queryset()


class MainSearchView(ListView):
    template_name = 'votephoto/searchMain.html'
    context_object_name = 'photo'

    def get_queryset(self):
        what_wrote_to_user = self.kwargs.get('search')
        self.queryset = Photo.objects.filter(
            (Q(name__icontains=what_wrote_to_user) | Q(content__icontains=what_wrote_to_user)), state='Verified')
        if self.queryset.count() == 0:
            photo_search = []
            user_search = User.objects.filter(username__icontains=what_wrote_to_user)
            if user_search != 0:
                for user_in_search in user_search:
                    user_photo = Photo.objects.filter(user=user_in_search.pk, state='Verified')
                    for photo_one in user_photo:
                        photo_search.append(photo_one)
                self.queryset = photo_search
            else:
                self.queryset = None
        elif User.objects.filter(username__icontains=what_wrote_to_user) != 0:
            photo_search_to_user = []
            user_search = User.objects.filter(username__icontains=what_wrote_to_user)
            for user_in_search in user_search:
                all_photo_to_one_user = Photo.objects.filter(user=user_in_search.pk, state='Verified')
                for one_photo_to_one_user in all_photo_to_one_user:
                    photo_search_to_user.append(one_photo_to_one_user)
            set_gueryset = set(self.queryset)
            set_photo_search_to_user = set(photo_search_to_user)
            self.queryset = list(set_gueryset.union(set_photo_search_to_user))
        else:
            self.queryset = None
        return super().get_queryset()


class SortedAllPhotoOneUser(ListView):
    template_name = 'votephoto/sortedAllPhotoOneUser.html'
    context_object_name = 'photo'

    def get_queryset(self):
        photo_all = []
        get_sorted_name = self.kwargs.get('sorting')
        if get_sorted_name == 'All photo':
            self.queryset = Photo.objects.filter(user=self.request.user.pk)
            return super().get_queryset()
        photo_one_user = Photo.objects.filter(user=self.request.user.pk)
        for photo_one in photo_one_user:
            if photo_one.state == get_sorted_name:
                photo_all.append(photo_one)
        self.queryset = list(set(photo_all))
        return super().get_queryset()


class ViewPhotoNotVerified(ListView):
    template_name = 'votephoto/viewPhotoNotVerified.html'
    context_object_name = 'photo'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Проверка фотографий'
        return context

    def get_queryset(self):
        if self.request.user.is_staff and self.request.user.is_superuser:
            set_gueryset = set(Photo.objects.filter(state='Not verified'))
            set_photo_search_to_user = set(Photo.objects.filter(state='On check'))
            self.queryset = list(set_gueryset.union(set_photo_search_to_user))
            return super().get_queryset()
        else:
            raise Http404(f'{self.request.user.username} не является админом! Зайдите на другой аккаунт!')


class ViewPhotoUpdate(ListView):
    template_name = 'votephoto/viewPhotoUpdate.html'
    context_object_name = 'photo'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Проверка фотографий'
        return context

    def get_queryset(self):
        if self.request.user.is_staff and self.request.user.is_superuser:
            self.queryset = Photo.objects.filter(state='Update')
            return super().get_queryset()
        else:
            raise Http404(f'{self.request.user.username} не является админом! Зайдите на другой аккаунт!')


class ViewPhotoDelete(ListView):
    template_name = 'votephoto/viewPhotoNotVerified.html'
    context_object_name = 'photo'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Проверка фотографий'
        return context

    def get_queryset(self):
        if self.request.user.is_staff and self.request.user.is_superuser:
            self.queryset = Photo.objects.filter(state='Delete')
            return super().get_queryset()
        else:
            raise Http404(f'{self.request.user.username} не является админом! Зайдите на другой аккаунт!')


def showPhotoAdmin(request, photoID):
    if request.user.is_staff and request.user.is_superuser:
        photo = get_object_or_404(Photo, pk=photoID)
        if photo.state == 'On check':
            photo.go_state_not_verified()
            photo.go_state_on_check()
            return render(request, 'votephoto/showPhotoAdmin.html', {'title': 'Проверка фотографии', 'photo': photo})
        else:
            photo.go_state_on_check()
            photo.save()
            return render(request, 'votephoto/showPhotoAdmin.html', {'title': 'Проверка фотографии', 'photo': photo})
    else:
        return Http404(Http404(f'{request.user.username} не является админом! Зайдите на другой аккаунт!'))


def showPhotoAdminUpdate(request, photoID):
    if request.user.is_staff and request.user.is_superuser:
        photo = get_object_or_404(Photo, pk=photoID)
        photo.save()
        return render(request, 'votephoto/showPhotoAdminUpdate.html', {'title': 'Проверка фотографии', 'photo': photo})
    else:
        return Http404(Http404(f'{request.user.username} не является админом! Зайдите на другой аккаунт!'))


def updateStateVerified(request, photoID):
    photo = get_object_or_404(Photo, pk=photoID)
    if request.method == 'POST':
        photo.go_state_verified()
        photo.save()
        return redirect('photoNotVerified')


def updateStateNotVerified(request, photoID):
    photo = get_object_or_404(Photo, pk=photoID)
    if request.method == 'POST':
        photo.go_state_not_verified()
        photo.save()
        return redirect('photoNotVerified')


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


def update_photo(request, photoID):
    up_photo = get_object_or_404(Photo, pk=photoID)
    up_photo.old_photo = up_photo.new_photo
    up_photo.new_photo = None
    up_photo.go_state_verified()
    up_photo.save()
    return redirect('photoUpdate')


def loading_new_photo(request, photoID):
    photo = get_object_or_404(Photo, pk=photoID)
    if request.method == 'POST':
        form = AddNewPhotoForm(request.POST, request.FILES)
        if form.is_valid():
            obj = form.save(commit=False)
            if form.data.get('new_photo') == '':
                photo.name = obj.name
                photo.content = obj.content
                photo.go_state_not_verified()
                photo.save()
                return redirect('all_photo')
            else:
                photo.name = obj.name
                photo.content = obj.content
                photo.new_photo = obj.new_photo
                photo.go_state_update()
                photo.save()
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
    context = {'title': f'Фотографии {request.user.username}-a', 'photo': photos}
    return render(request, 'votephoto/allPhotoOneUser.html', context)


@shared_task(name="celery_delete_photo")
def celery_delete_photo():
    photo_delete_all = Photo.objects.filter(state='Delete')
    count_photo_delete = Photo.objects.filter(state='Delete').count()
    for one_photo_delete in photo_delete_all:
        one_photo_delete.date_now = timezone.now()
        one_photo_delete.save()
        if one_photo_delete.date_now >= one_photo_delete.date_delete:
            one_photo_delete.delete()
    if count_photo_delete >= 1:
        return 'There are photos to delete.'
    else:
        return 'No photos to delete.'


def delete_photo(request, photoID):
    photo = get_object_or_404(Photo, pk=photoID)
    photo.date_delete = datetime.now() + timedelta(minutes=15)
    photo.go_state_photo_delete()
    photo.date_now = datetime.now() + timedelta(seconds=1)
    photo.save()
    return redirect('main')
