
from django import template
from django.utils import timezone

from datetime import datetime

register = template.Library()


@register.filter(name="str2dateStr")
def str2dateStr(value):
    return str(value).split("T")[0]
