from django import template

register = template.Library()

@register.filter
def percentage(value):
    try:
        return "{:.2f}%".format(float(value) * 100)
    except (ValueError, TypeError):
        return value
