from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token

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
    path('sortingMain/<str:sorting>/', MainSortedView.as_view(), name='sortingMain'),
    path('sortingAllPhotoOneUser/<str:sorting>', SortedAllPhotoOneUser.as_view(), name='sortingAllPhotoOneUser'),
    path('photoNotVerified/', ViewPhotoNotVerified.as_view(), name='photoNotVerified'),
    path('show_photo_admin/<int:photoID>/', showPhotoAdmin, name='showPhotoAdmin'),
    path('updateStateVerified/<int:photoID>/', updateStateVerified, name='updateStateVerified'),
    path('updateStateNotVerified/<int:photoID>/', updateStateNotVerified, name='updateStateNotVerified'),
    path('photoUpdate/', ViewPhotoUpdate.as_view(), name='photoUpdate'),
    path('photoDelete/', ViewPhotoDelete.as_view(), name='photoDelete'),
    path('show_photo_admin_update/<int:photoID>/', showPhotoAdminUpdate, name='showPhotoAdminUpdate'),
    path('updatePhotoInAdmin/<int:photoID>/', update_photo, name='updatePhotoInAdmin'),
    path('cancle_delete_photo/<int:photoID>/', cancel_delete_photo, name='cancelDeletePhoto'),
    path('token/', obtain_auth_token),
    path('rename_token/', rename_token, name='rename_token'),
    path('rename_profile/', rename_profile, name='rename_profile'),

]
