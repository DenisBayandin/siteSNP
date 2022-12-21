from django.contrib import admin
from .models import *


class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'email')
    list_display_links =  ('id', 'username')

class PhotoAdmin(admin.ModelAdmin):
    list_display = ('photoID', 'namePhoto', 'сontentPhoto')
    list_display_links = ('photoID', 'namePhoto', 'сontentPhoto')

class CommentAdmin(admin.ModelAdmin):
    list_display = ('commentID', 'contentComment')
    list_display_links = ('commentID', 'contentComment')

admin.site.register(User, UserAdmin)
admin.site.register(Photo, PhotoAdmin)
admin.site.register(Comment, CommentAdmin)
