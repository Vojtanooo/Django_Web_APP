from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()


@register.filter
@stringfilter
def my_split_strip(value):
    return value.split("-")[0].strip()


@register.filter
@stringfilter
def my_split(value):
    return value.split(",")[0].strip("['")
