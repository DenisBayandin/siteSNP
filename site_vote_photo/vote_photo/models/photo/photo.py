from django.db import models
from django.urls import reverse
from django_fsm import FSMField, transition

from vote_photo.models.user.user import User


class Photo(models.Model):
    name = models.CharField(max_length=100)
    content = models.TextField(blank=True)
    date_create = models.DateTimeField(auto_now_add=True)
    date_update = models.DateTimeField(auto_now=True)
    date_delete = models.DateTimeField(null=True)
    photo_delete = models.ImageField(
        blank=True, null=True, upload_to="delete_photos/%Y/%m/%d"
    )
    new_photo = models.ImageField(blank=True, upload_to="new_photos/%Y/%m/%d")
    old_photo = models.ImageField(blank=True, upload_to="old_photos/%Y/%m/%d")
    photo_145x165 = models.ImageField(blank=True, upload_to="photos_145x165/%Y/%m/%d")
    photo_510x510 = models.ImageField(blank=True, upload_to="photos_510x510/%Y/%m/%d")
    count_like = models.IntegerField(default=0)
    count_comment = models.IntegerField(default=0)
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    state = FSMField(
        default="Not verified", protected=True, verbose_name="Статус фотографии"
    )

    class Meta:
        db_table = "photos"
        verbose_name = "Фото"
        verbose_name_plural = "Фотографии"
        ordering = ("-date_create",)

    @transition(field=state, source="Not verified", target="On check")
    def go_state_on_check(self):
        return "Status changed from not verified to on check"

    @transition(field=state, source=["On check", "Update"], target="Verified")
    def go_state_verified(self):
        return "Status changed from on check to verified"

    @transition(
        field=state,
        source=["Not verified", "On check", "Verified", "Update"],
        target="Delete",
    )
    def go_state_photo_delete(self):
        return "State changed to delete"

    @transition(
        field=state,
        source=["Verified", "On check", "Delete", "Update"],
        target="Not verified",
    )
    def go_state_not_verified(self):
        return "Status changed to not verified"

    @transition(
        field=state,
        source=["Not verified", "Verified", "On check", "Delete"],
        target="Update",
    )
    def go_state_update(self):
        return "Status changed to update"

    def get_absolute_url(self):
        return reverse("show_photo", kwargs={"photoID": self.pk})

    def get_absolute_url_admin(self):
        return reverse("show_photo_admin", kwargs={"photoID": self.pk})

    def get_absolute_url_admin_update(self):
        return reverse("show_photo_admin_update", kwargs={"photoID": self.pk})

    def __str__(self):
        return f"Name photo: {self.name}"
