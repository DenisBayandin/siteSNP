from django.db.models import Q
from django.views.generic import ListView

from ..models import User, Photo


class MainView(ListView):
    # TODO Отображение фотографий с state=Verified на главной странице.
    template_name = "vote_photo/main.html"
    context_object_name = "photo"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Главная страница"
        return context

    def get_queryset(self):
        self.queryset = Photo.objects.filter(state="Verified")
        return super().get_queryset()


class MainSortedView(ListView):
    # TODO Сортировка фотографий на главной странице.
    template_name = "vote_photo/sortedMain.html"
    context_object_name = "photo"

    def get_queryset(self):
        get_sorted_name = self.kwargs.get("sorting")
        self.queryset = Photo.objects.filter(state="Verified").order_by(get_sorted_name)
        return super().get_queryset()


class MainSearchView(ListView):
    # TODO Поиск фотографий на главной странице.
    template_name = "vote_photo/searchMain.html"
    context_object_name = "photo"

    def get_queryset(self):
        what_wrote_to_user = self.kwargs.get("search")
        self.queryset = Photo.objects.filter(
            (
                Q(name__icontains=what_wrote_to_user)
                | Q(content__icontains=what_wrote_to_user)
            ),
            state="Verified",
        )
        if self.queryset.count() == 0:
            photo_search = []
            user_search = User.objects.filter(username__icontains=what_wrote_to_user)
            if user_search != 0:
                for user_in_search in user_search:
                    user_photo = Photo.objects.filter(
                        user=user_in_search.id, state="Verified"
                    )
                    for photo_one in user_photo:
                        photo_search.append(photo_one)
                self.queryset = photo_search
            else:
                self.queryset = None
        elif User.objects.filter(username__icontains=what_wrote_to_user) != 0:
            photo_search_to_user = []
            user_search = User.objects.filter(username__icontains=what_wrote_to_user)
            for user_in_search in user_search:
                all_photo_to_one_user = Photo.objects.filter(
                    user=user_in_search.id, state="Verified"
                )
                for one_photo_to_one_user in all_photo_to_one_user:
                    photo_search_to_user.append(one_photo_to_one_user)
            set_gueryset = set(self.queryset)
            set_photo_search_to_user = set(photo_search_to_user)
            self.queryset = list(set_gueryset.union(set_photo_search_to_user))
        return super().get_queryset()
