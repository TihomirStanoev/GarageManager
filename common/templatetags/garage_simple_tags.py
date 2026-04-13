from django import template
from django.utils import timezone
from GarageManager.settings import SITE_NAME
register = template.Library()

@register.simple_tag(takes_context=False)
def year():
    return f'{timezone.now().year}'


@register.simple_tag(takes_context=False)
def site_name():
    return SITE_NAME

@register.filter
def format_id(value):
    return f'#{value:05d}'

@register.filter
def currency(value):
    return f'{value:.2f}€'

@register.filter
def is_in_group(user, group_name):
    return group_name in user.groups.values_list('name', flat=True)