from django import template
from pharmacy import views

register = template.Library()

@register.simple_tag
def get_categories():
    return views.categories_db