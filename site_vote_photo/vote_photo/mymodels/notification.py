from .user import User

from django.db import models


class Notification(models.Model):
    sender = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Отправил уведомление",
        blank=True,
        null=True,
        related_name="sender",
    )
    recipient = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Получил уведомление",
        blank=True,
        null=True,
        related_name="recipient",
    )
    message = models.CharField(max_length=250, null=True, blank=True)
    date_create = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "notifications"
        verbose_name = "Уведомление"
        verbose_name_plural = "Уведомления"
