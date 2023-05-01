from .view.admin.admin import (
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
from .view.celery.celery_view import celery_delete_photo, delete_photo
from .view.comment.comment import delete_comment, update_comment
from .view.like.like import add_like
from .view.photo.photo_one import (
    show_one_photo,
    loading_new_photo,
    cancel_delete_photo,
)
from .view.photo.photo_user import SortedAllPhotoOneUser, view_all_photo
from .view.photo.photo import MainView, MainSortedView, MainSearchView
from .view.auth.auth import (
    RegisterUser,
    LoginUser,
    profile,
    logout_view,
    update_password,
)
from .view.update.update_data import update_token, update_data_profile
from .view.notification.notification import notification_view
