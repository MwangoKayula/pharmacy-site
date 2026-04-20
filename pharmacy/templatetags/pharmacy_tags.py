from django import template
from pharmacy.models import Category, Tag

register = template.Library()


@register.simple_tag
def get_categories():
    return Category.objects.all()


@register.inclusion_tag('pharmacy/categories_sidebar.html')
def show_categories(cat_selected=0):
    cats = Category.objects.all()
    return {'cats': cats, 'cat_selected': cat_selected}


@register.inclusion_tag('pharmacy/tags_sidebar.html')
def show_all_tags():
    tags = Tag.objects.all()
    return {'tags': tags}