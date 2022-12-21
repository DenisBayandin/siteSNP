from django import template
from ..models import *

register = template.Library()


@register.simple_tag(name='users')
def get_user():
    return User.objects.all()


@register.simple_tag
def get_atribute_user():
    return User._meta.fields


@register.simple_tag
def getAllLikesIsPhoto(photoID):
    photo = Photo.objects.get(pk=photoID)
    likes = Like.objects.filter(photo_id=photo.photoID).count()
    return likes


@register.simple_tag
def TrueAndFalseLikeUserPhoto(photoID, userID):
    try:
        if Like.objects.get(photo_id=photoID, user_id=userID):
            return True
    except:
        return False
