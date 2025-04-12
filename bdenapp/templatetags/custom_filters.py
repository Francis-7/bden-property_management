from django import template
from collections import Counter
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

@register.filter
def get_city_counts(properties, state_name):
    """
    Extract city names and count their occurrences for properties in the same state.
    """
    try:
        # Count cities in the given state
        city_counts = Counter(
            property.location.split(',')[1].strip()
            for property in properties
            if property.location and len(property.location.split(',')) > 1 and property.location.split(',')[0].strip() == state_name
        )
        return city_counts.items()  # Return as list of tuples (city, count)
    except Exception as e:
        return []  # Return empty list in case of any issue
    
# division by 2
@register.filter
def divide(value, arg):
    try:
        return f"{float(value) / float(arg):.2f}"
    except (ValueError, ZeroDivisionError):
        return None
