from django.views.generic import ListView

from ..models import Photo
from ..services.page_main_search_photo import ServiceMainSearchPhoto


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
        self.queryset = ServiceMainSearchPhoto.execute({"search": what_wrote_to_user})
        return super().get_queryset()
