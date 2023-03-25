from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from ..view.photo_view import (
    AllPhotoView,
    AllPhotoWithStateVerifiedView,
    OnePhotoView,
    LoadPhotoView,
)
from ..view.comment_view import CommentOnePhotoView, OneCommentView


urlpatterns = [
    path("photos/", AllPhotoView.as_view()),
    path("photos/verified_photo/", AllPhotoWithStateVerifiedView.as_view()),
    path("photos/one_photo/<int:pk>/", OnePhotoView.as_view()),
    path("photos/load_new_photo/", LoadPhotoView.as_view()),
    path("photos/<int:photo_id>/comments/", CommentOnePhotoView.as_view()),
    path("comments/one_comment/<int:comment_id>/", OneCommentView.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
