from django import template
from ..models import *

register = template.Library()


@register.simple_tag(name = 'users')
def get_user():
    return User.objects.all()

@register.simple_tag(name = 'AtributeUser')
def get_atribute_user():
    return User._meta.fields

print(get_atribute_user)