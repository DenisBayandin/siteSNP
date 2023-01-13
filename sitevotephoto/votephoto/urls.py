from django.urls import path
from .views import *

urlpatterns = [
    path('', MainView.as_view(), name='main'),
    path('login/', LoginUser.as_view(), name='login'),
    path('register/', RegisterUser.as_view(), name='register'),
    path('accounts/profile/', profile, name='profile'),
    path('logout/', logout_view, name='logout'),
    path('show_photo/<int:photoID>/', showOnePhoto, name='show_photo'),
    path('addlike/', addlike, name='addlike'),
    path('deleteComment/<int:commentID>/<int:photoID>/', delete_comment, name='delete_comment'),
    path('updateComment/<int:commentID>/<int:photoID>/', update_comment, name='update_comment'),
    path('allPhotoOneUser/', viewAllPhoto, name='all_photo'),
    path('deletePhoto/<int:photoID>/', delete_photo, name='delete_photo'),
    path('loadingNewPhoto/<int:photoID>/', loading_new_photo, name='loading_new_photo'),
    path('searchMain/<str:search>/', MainSearchView.as_view(), name='search_photos'),
    path('sortingMain/<str:sorting>/', MainSortedView.as_view(), name='sortingMain')

]
