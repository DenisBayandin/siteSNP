from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token

from .views import (
    MainView,
    LoginUser,
    RegisterUser,
    profile,
    logout_view,
    show_one_photo,
    add_like,
    delete_comment,
    update_comment,
    view_all_photo,
    delete_photo,
    loading_new_photo,
    MainSearchView,
    MainSortedView,
    SortedAllPhotoOneUser,
    ViewPhotoNotVerified,
    show_photo_admin,
    ViewPhotoDelete,
    ViewPhotoUpdate,
    show_photo_admin_update,
    cancel_delete_photo,
    update_token,
    update_data_profile,
    update_photo,
    update_state_verified,
    update_state_not_verified,
    update_password,
    notification_view,
    send_notification_all_user,
)


urlpatterns = [
    path("", MainView.as_view(), name="main"),
    path("login/", LoginUser.as_view(), name="login"),
    path("register/", RegisterUser.as_view(), name="register"),
    path("accounts/profile/", profile, name="profile"),
    path("logout/", logout_view, name="logout"),
    path("show_photo/<int:photoID>/", show_one_photo, name="show_photo"),
    path("add_like/", add_like, name="add_like"),
    path(
        "delete_comment/<int:commentID>/<int:photoID>/",
        delete_comment,
        name="delete_comment",
    ),
    path(
        "update_comment/<int:commentID>/<int:photoID>/",
        update_comment,
        name="update_comment",
    ),
    path("all_photo_one_user/", view_all_photo, name="all_photo"),
    path("delete_photo/<int:photoID>/", delete_photo, name="delete_photo"),
    path(
        "loading_new_photo/<int:photoID>/", loading_new_photo, name="loading_new_photo"
    ),
    path("search_main/<str:search>/", MainSearchView.as_view(), name="search_photos"),
    path("sorting_main/<str:sorting>/", MainSortedView.as_view(), name="sorting_main"),
    path(
        "sorting_all_photo_one_user/<str:sorting>",
        SortedAllPhotoOneUser.as_view(),
        name="sorting_all_photo_one_user",
    ),
    path(
        "photo_not_verified/", ViewPhotoNotVerified.as_view(), name="photo_not_verified"
    ),
    path("show_photo_admin/<int:photoID>/", show_photo_admin, name="show_photo_admin"),
    path(
        "update_state_verified/<int:photoID>/",
        update_state_verified,
        name="update_state_verified",
    ),
    path(
        "update_state_not_verified/<int:photoID>/",
        update_state_not_verified,
        name="update_state_not_verified",
    ),
    path("photo_update/", ViewPhotoUpdate.as_view(), name="photo_update"),
    path(
        "show_photo_admin_update/<int:photoID>/",
        show_photo_admin_update,
        name="show_photo_admin_update",
    ),
    path(
        "update_photo_in_admin/<int:photoID>/",
        update_photo,
        name="update_photo_in_admin",
    ),
    path(
        "cancle_delete_photo/<int:photoID>/",
        cancel_delete_photo,
        name="cancle_delete_photo",
    ),
    path("rename_token/", update_token, name="rename_token"),
    path("rename_profile/", update_data_profile, name="rename_profile"),
    path("update_password/", update_password, name="update_password"),
    path("notification/", notification_view, name="notification_show"),
    path(
        "send_notification/all_user/",
        send_notification_all_user,
        name="notification_all_user",
    ),
]
