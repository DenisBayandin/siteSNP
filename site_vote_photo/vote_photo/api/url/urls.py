from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from ..view.photo_view import (
    AllPhotoView,
    AllPhotoWithStateVerifiedView,
    OnePhotoView,
    LoadPhotoView,
)
from ..view.comment_view import CommentOnePhotoView, OneCommentView
from ..view.like_view import LikesView, OneLikeView
from ..view.user_view import UsersView, DetailUser


urlpatterns = [
    path("photos/", AllPhotoView.as_view()),
    path("photos/verified_photo/", AllPhotoWithStateVerifiedView.as_view()),
    path("photos/one_photo/<int:id>/", OnePhotoView.as_view()),
    path("photos/load_new_photo/", LoadPhotoView.as_view()),
    path("photos/<int:photo_id>/comments/", CommentOnePhotoView.as_view()),
    path("comments/one_comment/<int:comment_id>/", OneCommentView.as_view()),
    path("photos/<int:photo_id>/likes/", LikesView.as_view()),
    path("likes/one_like/<int:like_id>/", OneLikeView.as_view()),
    path("users/", UsersView.as_view()),
    path("users/one_user/<int:user_id>/", DetailUser.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
