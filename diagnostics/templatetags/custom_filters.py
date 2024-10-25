import ast
from django import template

register = template.Library()

@register.filter(name='to_list')
def to_list(value):
    try:
        return ast.literal_eval(value)
    except (ValueError, SyntaxError):
        return []
