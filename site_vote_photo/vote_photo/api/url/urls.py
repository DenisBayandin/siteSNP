from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.urlpatterns import format_suffix_patterns

from ..view.photo_view import (
    AllPhotoView,
    AllPhotoWithStateVerifiedView,
    СhangeOnePhotoView,
    PhotosUserFilter,
    GetOnePhotoView,
)
from ..view.comment_view import (
    AllCommentOnePhotoView,
    OneCommentView,
    CreateCommentOnePhotoView,
    СhangeOneCommentView,
)
from ..view.like_view import LikesView, OneLikeView
from ..view.user_view import UsersView, DetailUser
from ..view.refresh_token_view import RefreshTokenView


urlpatterns = [
    path("photos/", AllPhotoView.as_view()),
    path("photos/verified_photo/", AllPhotoWithStateVerifiedView.as_view()),
    path("photos/one_photo/<int:photo_id>/", GetOnePhotoView.as_view()),
    path("photos/one_photo/change/<int:id>/", СhangeOnePhotoView.as_view()),
    path("photos/<int:photo_id>/likes/", LikesView.as_view()),
    path("likes/one_like/<int:like_id>/", OneLikeView.as_view()),
    path("users/", UsersView.as_view()),
    path("users/one_user/<int:user_id>/", DetailUser.as_view()),
    path("login/", obtain_auth_token),
    path("login/refresh/", RefreshTokenView.as_view()),
    path("user/photos/<str:filter>/", PhotosUserFilter.as_view()),
    path("comments/create/photos/<int:photo_id>/", CreateCommentOnePhotoView.as_view()),
    path(
        "comments/one_comment/change/<int:comment_id>/", СhangeOneCommentView.as_view()
    ),
    path("comments/view_all_comment/<int:photo_id>/", AllCommentOnePhotoView.as_view()),
    path("comments/view_one_comment/<int:comment_id>/", OneCommentView.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
