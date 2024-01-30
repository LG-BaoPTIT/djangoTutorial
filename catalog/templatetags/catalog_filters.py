# catalog_filters.py
from django import template
import locale

register = template.Library()

@register.filter(name='currency')
def currency(value):
    try:
        numeric_value = float(value)
    except (ValueError, TypeError):
        return value  # or handle it differently based on your requirements

    try:
        locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')
    except:
        locale.setlocale(locale.LC_ALL, '')
    loc = locale.localeconv()
    return locale.currency(numeric_value, loc['currency_symbol'], grouping=True)
