from django import template
register = template.Library()

@register.filter
def first_word_before_comma(value):
    return value.split(',')[0] if value else ''

@register.filter(name='to_list')  
def to_list(value):
    return list(value)

@register.filter
def to(value, arg):
    """
    Returns a range of integers from 'value' to 'arg - 1'.
    """
    return range(value, arg)