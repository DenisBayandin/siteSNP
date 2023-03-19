from django.apps import AppConfig
from django.db.models.signals import post_save


class VotephotoConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "votephoto"
    verbose_name = "Голосование за лучшее фото."

    def ready(self):
        from .signals import add_comment_counter
