from django.views.generic import ListView

from ..models import Photo
from .rename_lifetime_token import rename_lifetime_token_vk
from django.shortcuts import render, redirect


class SortedAllPhotoOneUser(ListView):
    # TODO Сортировка всех фотографий одного пользователя.
    #  (сортировка на вкладке 'Мои фотографии')
    template_name = "vote_photo/sortedAllPhotoOneUser.html"
    context_object_name = "photo"

    def get_queryset(self):
        if rename_lifetime_token_vk(self.request, self.request.user):
            return redirect("login")
        photo_all = []
        get_sorted_name = self.kwargs.get("sorting")
        if get_sorted_name == "All photo":
            self.queryset = Photo.objects.filter(user=self.request.user.id)
            return super().get_queryset()
        photo_one_user = Photo.objects.filter(user=self.request.user.id)
        for photo_one in photo_one_user:
            if photo_one.state == get_sorted_name:
                photo_all.append(photo_one)
        self.queryset = list(set(photo_all))
        return super().get_queryset()


def view_all_photo(request):
    # TODO Функция показа всех фотографий одного пользователя.
    """
    Все фотографии одного пользователя.
    Получаем фотографии текущего пользователя.
    """
    if rename_lifetime_token_vk(request, request.user):
        return redirect("login")
    photos = Photo.objects.filter(user=request.user)
    context = {"title": f"Фотографии {request.user.username}-a", "photo": photos}
    return render(request, "vote_photo/allPhotoOneUser.html", context)
