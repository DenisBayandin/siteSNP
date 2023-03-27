from django.apps import AppConfig


class VotephotoConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "vote_photo"
    verbose_name = "Голосование за лучшее фото."

    def ready(self):
        from .signals import add_comment_counter
