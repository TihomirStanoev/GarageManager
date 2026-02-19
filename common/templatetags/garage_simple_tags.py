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