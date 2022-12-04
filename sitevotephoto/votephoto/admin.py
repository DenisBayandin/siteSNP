from django.contrib import admin
from .models import *


class VotephotoAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'email')
    list_display_links =  ('id', 'username')

admin.site.register(User, VotephotoAdmin)
