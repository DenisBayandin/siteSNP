from django.urls import path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework import permissions

from vote_photo.api.api_view.photo.photo import (
    ListCreatePhotoView,
    RetrieveUpdateDestroyPhotoView,
    ListPhotoFilterView,
)
from vote_photo.api.api_view.comment.comment import (
    ListCommentView,
    RetrieveUpdateDestroyCommentView,
    CreateCommentView,
)
from vote_photo.api.api_view.like.like import ListPhotoLikeView, CreateDeleteLikeView
from vote_photo.api.api_view.user.user import ListCreateUserView, UpdateUserView
from vote_photo.api.api_view.admin.admin import (
    AdminChangingStatePhotoView,
    AdminUpdatePhotoView,
)
from vote_photo.api.api_view.token.custom_auth_token import (
    RetrieveCreateCustomAuthTokenView,
)
from vote_photo.api.api_view.token.custom_refresh_token import RefreshTokenView

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
    path("photos/", ListCreatePhotoView.as_view()),
    path("photos/<int:id>", RetrieveUpdateDestroyPhotoView.as_view()),
    path("photos/user", ListPhotoFilterView.as_view()),
    path("users/", ListCreateUserView.as_view()),
    path("users/<int:id>", UpdateUserView.as_view()),
    path("auth/token", RetrieveCreateCustomAuthTokenView.as_view()),
    path("auth/", RefreshTokenView.as_view()),
    path("comments/<int:id>", RetrieveUpdateDestroyCommentView.as_view()),
    path("comments/photo", ListCommentView.as_view()),
    path("comments/photo/<int:id>", CreateCommentView.as_view()),
    path("likes/", ListPhotoLikeView.as_view()),
    path("likes/<int:id>", CreateDeleteLikeView.as_view()),
    path(
        "admin/photo/<int:id>/changing_state/<str:state>",
        AdminChangingStatePhotoView.as_view(),
    ),
    path("admin/photo/<int:id>/apply_change_photo", AdminUpdatePhotoView.as_view()),
    path(
        "swagger/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
]

# breakpoint()
# urlpatterns = format_suffix_patterns(urlpatterns, allowed=['json'])
