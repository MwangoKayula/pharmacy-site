from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import Product, Category
from django.shortcuts import get_object_or_404
from .models import Category, Product
from .models import Product, Tag

menu = [
    {'title': 'Home', 'url_name': 'home'},
    {'title': 'About', 'url_name': 'about'},
    {'title': 'Add Product', 'url_name': 'add_product'},
    {'title': 'Contact', 'url_name': 'contact'},
    {'title': 'Login', 'url_name': 'login'},
]

def show_tag_products(request, tag_slug):
    tag = get_object_or_404(Tag, slug=tag_slug)
    products = tag.products.filter(is_published=True)   # using related_name='products'
    context = {
        'title': f'Tag: {tag.name}',
        'menu': menu,
        'products': products,
        'tag_selected': tag.slug,
    }
    return render(request, 'pharmacy/index.html', context)

def index(request):
    products = Product.published.all()
    context = {
        'title': 'Pharmacy Home',
        'menu': menu,
        'products': products,
    }
    return render(request, 'pharmacy/index.html', context)

def about(request):
    context = {'title': 'About Our Pharmacy', 'menu': menu}
    return render(request, 'pharmacy/about.html', context)

def show_product(request, product_slug):
    product = get_object_or_404(Product, slug=product_slug, is_published=True)
    context = {
        'title': product.name,
        'menu': menu,
        'product': product,
    }
    return render(request, 'pharmacy/product.html', context)

def show_category(request, cat_slug):
    
    category = get_object_or_404(Category, slug=cat_slug)    
    products = Product.published.filter(category=category)
    context = {
        'title': f'Category: {category.name}',
        'menu': menu,
        'products': products,
        'cat_selected': category.id,
    }
    return render(request, 'pharmacy/index.html', context)

# Placeholders for other menu items
def add_product(request):
    return HttpResponse("<h1>Add New Product</h1><p>Form will go here.</p>")

def contact(request):
    return HttpResponse("<h1>Contact Us</h1><p>Email: pharmacy@example.com</p>")

def login(request):
    return HttpResponse("<h1>Login</h1><p>Please log in.</p>")