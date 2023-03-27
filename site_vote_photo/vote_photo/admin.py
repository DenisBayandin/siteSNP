from django.contrib import admin
from django.contrib.admin import AdminSite

from .models import User, Photo, Comment, Like

admin.site.site_title = "VotePhoto"
admin.site.site_header = "Модерирование сайта VotePhoto"
admin.site.index_title = "Модерирование VotePhoto"


class UserAdmin(admin.ModelAdmin):
    list_display = (
        "username",
        "last_name",
        "first_name",
        "email",
        "date_create",
        "date_update",
    )
    list_display_links = ("username", "last_name", "first_name", "email")
    list_filter = ("date_create", "date_update", "is_superuser")
    search_fields = (
        "username__icontains",
        "first_name__icontains",
        "last_name__icontains",
        "email__icontains",
        "date_create__icontains",
        "date_update__icontains",
    )
    fields = (
        "username",
        "last_name",
        "first_name",
        "patronymic",
        "email",
        "photo_by_user",
        "password",
        "is_superuser",
        "is_staff",
        "is_active",
        ("last_login", "date_joined"),
    )


class PhotoAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "content",
        "state",
        "date_create",
        "date_update",
    )
    list_display_links = ("name", "content")
    list_filter = ("state",)
    search_fields = (
        "name__icontains",
        "username__icontains",
        "date_create__icontains",
        "date_update__icontains",
    )


class CommentAdmin(admin.ModelAdmin):
    list_display = ("content", "parent")
    list_display_links = ("content",)
    search_fields = ("content__icontains",)


class LikeAdmin(admin.ModelAdmin):
    list_display = ("photo", "user")
    list_filter = ("date_create",)


admin.site.register(User, UserAdmin)
admin.site.register(Photo, PhotoAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Like, LikeAdmin)
AdminSite.index_template = "admin/my_custom_index.html"
