from django import template

from ..models import *

register = template.Library()


@register.simple_tag(name="users")
def get_user():
    return User.objects.all()


@register.simple_tag
def get_atribute_user():
    return User._meta.fields


@register.simple_tag
def getAllLikesIsPhoto(photoID):
    photo = Photo.objects.get(pk=photoID)
    likes = Like.objects.filter(photo=photo.pk).count()
    return likes


@register.simple_tag
def TrueAndFalseLikeUserPhoto(photoID, userID):
    try:
        if Like.objects.get(photo=photoID, user=userID):
            return True
    except:
        return False


@register.simple_tag
def CountCommentOnePhotoToMain(photoID):
    countCommentOnePhoto = Comment.objects.filter(photo=photoID)
    return countCommentOnePhoto[:3]


@register.simple_tag
def CountComment(photoID):
    countComment = Comment.objects.filter(photo=photoID).count()
    return countComment


@register.simple_tag
def checking_for_photos(userID):
    user = User.objects.get(pk=userID)
    try:
        checking_url = user.photo_by_user.url
        return True
    except:
        return False
