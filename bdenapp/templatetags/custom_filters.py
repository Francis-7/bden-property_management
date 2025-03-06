from django import template
register = template.Library()

@register.filter
def first_word_before_comma(value):
    return value.split(',')[0] if value else ''