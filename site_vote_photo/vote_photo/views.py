from .view.admin import (
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
from .view.celery_view import celery_delete_photo, delete_photo
from .view.comment import delete_comment, update_comment
from .view.like import add_like
from .view.one_photo import (
    show_one_photo,
    loading_new_photo,
    cancel_delete_photo,
)
from .view.photo_one_user import SortedAllPhotoOneUser, view_all_photo
from .view.photo import MainView, MainSortedView, MainSearchView
from .view.reg_aut_login import (
    RegisterUser,
    LoginUser,
    profile,
    logout_view,
    update_password,
)
from .view.rename import rename_token, rename_profile
from .view.notification import notification_view
