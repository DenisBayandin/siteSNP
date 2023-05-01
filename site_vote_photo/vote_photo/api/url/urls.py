from django.urls import path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework import permissions
from rest_framework.authtoken.views import obtain_auth_token

from ..api_view.photo import (
    AllPhotoView,
    СhangeOnePhotoView,
    PhotosUserFilter,
    GetOnePhotoView,
)
from ..api_view.comment import (
    AllCommentOnePhotoView,
    OneCommentView,
    CreateCommentOnePhotoView,
    СhangeOneCommentView,
)
from ..api_view.like import AllLikesOnePhotoView, CreateLikeView
from ..api_view.user import UsersView, DetailUser
from ..api_view.refresh_token import RefreshTokenView
from ..api_view.admin import AdminChangingStatePhotoView, AdminUpdatePhotoView
from ..api_view.custom_auth_token import CustomGetAuthTokenView

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
    path("photos/<int:photo_id>/", GetOnePhotoView.as_view()),
    path("photos/<int:id>/", СhangeOnePhotoView.as_view()),
    path("photos/<str:filter>/", PhotosUserFilter.as_view()),
    path("users/", UsersView.as_view()),
    path("users/<int:user_id>/", DetailUser.as_view()),
    path("token/", CustomGetAuthTokenView.as_view()),
    path("token/refresh/", RefreshTokenView.as_view()),
    path("comment/<int:photo_id>/", CreateCommentOnePhotoView.as_view()),
    path("comment/<int:comment_id>/", СhangeOneCommentView.as_view()),
    path("comments/<int:photo_id>/", AllCommentOnePhotoView.as_view()),
    path("comment/<int:one_comment_id>/", OneCommentView.as_view()),
    path("likes/<int:photo_id>/", AllLikesOnePhotoView.as_view()),
    path("like/<int:photo_id>/", CreateLikeView.as_view()),
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
