from .myviews.admin_view import (
    ViewPhotoNotVerified,
    ViewPhotoUpdate,
    ViewPhotoDelete,
    show_photo_admin,
    show_photo_admin_update,
    update_state_verified,
    update_state_not_verified,
    update_photo,
)
from .myviews.celery_view import celery_delete_photo, delete_photo
from .myviews.comment_view import delete_comment, update_comment
from .myviews.like_view import add_like
from .myviews.one_photo_view import (
    show_one_photo,
    loading_new_photo,
    cancel_delete_photo,
)
from .myviews.photo_one_user import SortedAllPhotoOneUser
from .myviews.photo_view import MainView, MainSortedView, MainSearchView, view_all_photo
from .myviews.reg_aut_login_view import RegisterUser, LoginUser, profile, logout_view
from .myviews.rename_view import rename_token, rename_profile
