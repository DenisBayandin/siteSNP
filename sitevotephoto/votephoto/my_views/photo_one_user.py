from django.views.generic import ListView

from ..models import *


class SortedAllPhotoOneUser(ListView):
    # TODO Сортировка всех фотографий одного пользователя. (сортировка на вкладке 'Мои фотографии')
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
