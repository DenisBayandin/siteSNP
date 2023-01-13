from django.contrib import admin
from .models import User, Photo, Comment, Like


class UserAdmin(admin.ModelAdmin):
    list_display = ('pk', 'username', 'email')
    list_display_links = ('pk', 'username')
    fields = ('username',
              'last_name',
              'first_name',
              'patronymic',
              'email',
              'photo_by_user',
              'password',
              'is_superuser',
              'is_staff',
              'is_active',
              'moderator',
              ('last_login',
               'date_joined'),
              )


class PhotoAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'content')
    list_display_links = ('pk', 'name', 'content')


class CommentAdmin(admin.ModelAdmin):
    list_display = ('pk', 'content')
    list_display_links = ('pk', 'content')


admin.site.register(User, UserAdmin)
admin.site.register(Photo, PhotoAdmin)
admin.site.register(Comment, CommentAdmin)
