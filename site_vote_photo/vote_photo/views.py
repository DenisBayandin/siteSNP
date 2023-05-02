from .views.admin.admin import (
    ViewPhotoNotVerified,
    ViewPhotoUpdate,
    ViewPhotoDelete,
    show_photo_admin,
    show_photo_admin_update,
    update_state_verified,
    update_state_not_verified,
    update_photo,
    send_notification_all_user,
)
from .views.celery.celery_view import celery_delete_photo, delete_photo
from .views.comment.comment import delete_comment, update_comment
from .views.like.like import add_like
from .views.photo.photo_one import (
    show_one_photo,
    loading_new_photo,
    cancel_delete_photo,
)
from .views.photo.photo_user import SortedAllPhotoOneUser, view_all_photo
from .views.photo.photo import MainView, MainSortedView, MainSearchView
from .views.auth.auth import (
    RegisterUser,
    LoginUser,
    profile,
    logout_view,
    update_password,
)
from .views.update.update_data import update_token, update_data_profile
from .views.notification.notification import notification_view
