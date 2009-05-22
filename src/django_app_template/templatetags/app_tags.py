from django import template
from django.conf import settings

register = template.Library()

@register.inclusion_tag('app_template/message.html')
def counter(object):
    return dict('settings': settings)
