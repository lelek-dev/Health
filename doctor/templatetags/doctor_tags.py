from django.contrib.auth.models import Group
from django import template
register = template.Library()


@register.filter(name='is_group') 
def is_group(user, group_name):
    try:
        group = Group.objects.get(name=group_name) 
        return group in user.groups.all() 
    except Group.DoesNotExist:
        return False