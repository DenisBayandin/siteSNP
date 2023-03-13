from channels.layers import get_channel_layer
from .my_views.admin_view import *
from.my_views.celery_view import *
from .my_views.comment_view import *
from .my_views.like_view import *
from .my_views.one_photo_view import *
from .my_views.photo_one_user import *
from .my_views.photo_view import *
from .my_views.reg_aut_login_view import *
from .my_views.rename_view import *

version_vk_api = '5.131'
channel_layer = get_channel_layer()
