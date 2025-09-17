from django import template

register = template.Library()

@register.filter
def lookup(dictionary, key):
    """Template filter to lookup a key in a dictionary"""
    return dictionary.get(key, [])

@register.simple_tag
def format_date_string(year, month, day):
    """Template tag to format date as YYYY-MM-DD"""
    return f"{year}-{month:02d}-{day:02d}"
