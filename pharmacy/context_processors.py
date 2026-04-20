from .models import Category, Tag

def pharmacy_context(request):
    return {
        'categories': Category.objects.all(),
        'tags': Tag.objects.all(),
    }