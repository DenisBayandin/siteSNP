from django import template
from django.core.exceptions import ObjectDoesNotExist

from ..models import User, Photo, Comment, Like

register = template.Library()


@register.simple_tag(name="users")
def get_user():
    return User.objects.all()


@register.simple_tag
def get_atribute_user():
    return User._meta.fields


@register.simple_tag
def get_all_likes_is_photo(photoID):
    photo = Photo.objects.get(id=photoID)
    likes = Like.objects.filter(photo=photo.id).count()
    return likes


@register.simple_tag
def true_and_false_like_user_photo(photoID, userID):
    try:
        if Like.objects.get(photo=photoID, user=userID):
            return True
    except ObjectDoesNotExist:
        return False


@register.simple_tag
def count_comment_one_photo_to_main(photoID):
    count_comment_one_photo = Comment.objects.filter(photo=photoID)
    return count_comment_one_photo[:3]


@register.simple_tag
def count_comment(photoID):
    count_comment = Comment.objects.filter(photo=photoID).count()
    return count_comment


@register.simple_tag
def checking_for_photos(userID):
    user = User.objects.get(id=userID)
    if user.url_photo_by_user_from_VK is None:
        return True
    else:
        return False
