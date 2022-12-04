from django import template
from ..models import *

register = template.Library()


@register.simple_tag(name = 'users')
def get_user():
    return User.objects.all()
