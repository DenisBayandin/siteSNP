from django.urls import path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework import permissions

from ..view.photo_view import (
    AllPhotoView,
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
from ..view.like_view import AllLikesOnePhotoView, CreateLikeView, ChangeLikeView
from ..view.user_view import UsersView, DetailUser
from ..view.refresh_token_view import RefreshTokenView
from ..view.admin_view import AdminChangingStatePhotoView, AdminUpdatePhotoView
from ..view.custom_auth_token_view import CustomGetAuthTokenView

schema_view = get_schema_view(
    openapi.Info(
        title="Vote Photo API",
        default_version="v1",
        description="API for the website VotePhoto",
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path("photos/", AllPhotoView.as_view()),
    path("photos/one_photo/get/<int:photo_id>/", GetOnePhotoView.as_view()),
    path("photos/one_photo/change/<int:id>/", СhangeOnePhotoView.as_view()),
    path("users/", UsersView.as_view()),
    path("users/one_user/<int:user_id>/", DetailUser.as_view()),
    path("login/", CustomGetAuthTokenView.as_view()),
    path("login/refresh_token/", RefreshTokenView.as_view()),
    path("user/photos/<str:filter>/", PhotosUserFilter.as_view()),
    path("comments/create/photos/<int:photo_id>/", CreateCommentOnePhotoView.as_view()),
    path(
        "comments/one_comment/change/<int:comment_id>/", СhangeOneCommentView.as_view()
    ),
    path("comments/view_all_comment/<int:photo_id>/", AllCommentOnePhotoView.as_view()),
    path("comments/view_one_comment/<int:comment_id>/", OneCommentView.as_view()),
    path("likes/all_likes/photo/<int:photo_id>/", AllLikesOnePhotoView.as_view()),
    path("likes/create_like/photo/<int:photo_id>/", CreateLikeView.as_view()),
    path("likes/change_like/photo/<int:photo_id>/", ChangeLikeView.as_view()),
    path(
        "admin/changing_state/<str:state>/<int:photo_id>/",
        AdminChangingStatePhotoView.as_view(),
    ),
    path("admin/update_photo/<int:photo_id>/", AdminUpdatePhotoView.as_view()),
    path(
        "swagger/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
]

urlpatterns = format_suffix_patterns(urlpatterns)
