from django import template
from pharmacy.models import Category

register = template.Library()

@register.simple_tag
def get_categories():
    return Category.objects.all()

@register.inclusion_tag('pharmacy/categories_sidebar.html')
def show_categories():
    cats = Category.objects.all()
    return {'cats': cats}