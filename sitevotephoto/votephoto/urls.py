from django.contrib import admin
from django.urls import path, include
from .views import *

urlpatterns = [
    path('', main_view, name = 'main'),
    path('login/', LoginUser.as_view(), name = 'login'),
    path('register/', RegisterUser.as_view(), name = 'register'),
    path('accounts/profile/', profile, name = 'profile'),
    path('logout/', logout_view, name = 'logout'),
    path('__debug__/', include('debug_toolbar.urls')),
    path('show_photo/<int:photoID>/', showOnePhoto, name = 'show_photo'),
    path('addlike/<int:photoID>', addlike, name='addlike'),
]
