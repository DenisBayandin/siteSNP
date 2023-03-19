from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete
from .mymodels.model_comment import Comment
from .mymodels.model_photo import Photo
from .mymodels.model_like import Like


@receiver(post_save, sender=Comment)
def add_comment_counter(sender, instance, **kwargs):
    get_pk_photo = instance.photo_id
    get_photo = Photo.objects.get(pk=get_pk_photo)
    get_photo.count_comment += 1
    get_photo.save()
    return 0


@receiver(post_delete, sender=Comment)
def delete_comment_counter(sender, instance, **kwargs):
    get_pk_photo = instance.photo_id
    get_photo = Photo.objects.get(pk=get_pk_photo)
    get_photo.count_comment -= 1
    get_photo.save()
    return 0


@receiver(post_save, sender=Like)
def add_like_counter(sender, instance, **kwargs):
    get_pk_photo = instance.photo_id
    get_photo = Photo.objects.get(pk=get_pk_photo)
    get_photo.count_like += 1
    get_photo.save()
    return 0


@receiver(post_delete, sender=Like)
def delete_like_counter(sender, instance, **kwargs):
    get_pk_photo = instance.photo_id
    get_photo = Photo.objects.get(pk=get_pk_photo)
    get_photo.count_like -= 1
    get_photo.save()
    return 0
