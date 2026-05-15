from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.urls import reverse
from django.utils.text import slugify
from .models import Product, Category, Tag
from .forms import AddProductForm
from django.contrib.auth.decorators import login_required

# ===== Helper functions (if any) =====

# ===== Main views =====
def index(request):
    products = Product.published.all()
    context = {
        'title': 'Pharmacy Home',
        'products': products,
    }
    return render(request, 'pharmacy/index.html', context)

def about(request):
    context = {'title': 'About Our Pharmacy'}
    return render(request, 'pharmacy/about.html', context)

def show_product(request, product_slug):
    product = get_object_or_404(Product, slug=product_slug, is_published=True)
    context = {
        'title': product.name,
        'product': product,
    }
    return render(request, 'pharmacy/product.html', context)

def show_category(request, cat_slug):
    category = get_object_or_404(Category, slug=cat_slug)
    products = Product.published.filter(category=category)
    context = {
        'title': f'Category: {category.name}',
        'products': products,
        'cat_selected': category.id,
    }
    return render(request, 'pharmacy/index.html', context)

def show_tag_products(request, tag_slug):
    tag = get_object_or_404(Tag, slug=tag_slug)
    products = tag.products.filter(is_published=True)
    context = {
        'title': f'Tag: {tag.name}',
        'products': products,
        'tag_selected': tag.slug,
    }
    return render(request, 'pharmacy/index.html', context)

@login_required
def add_product(request):
    if request.method == 'POST':
        form = AddProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.author = request.user
            product.save()
        return redirect('home')
    else:
        form = AddProductForm()
    context = {
        'title': 'Add Product',
        'form': form,
    }
    return render(request, 'pharmacy/add_product.html', context)

# ===== Placeholders for other menu items =====
def contact(request):
    return HttpResponse("<h1>Contact Us</h1><p>Email: pharmacy@example.com</p>")

# login placeholder - using the users app, so this view may be removed.
# Keeping it for backward compatibility but it will not be used if login is handled by users app.
def login(request):
    return HttpResponse("<h1>Login</h1><p>Please use the dedicated login page: /users/login/</p>")

# ===== Archive and error handling (from earlier works) =====
def categories(request, cat_id):
    return HttpResponse(f"<h1>Medication Category</h1><p>Category ID: {cat_id}</p>")

def categories_by_slug(request, cat_slug):
    if request.GET:
        print("GET parameters:", request.GET)
    return HttpResponse(f"<h1>Medication Category</h1><p>Slug: {cat_slug}</p>")

def archive(request, year):
    if year > 2025:
        return redirect('home')
    return HttpResponse(f"<h1>Pharmacy Archive</h1><p>Year: {year}</p>")

def page_not_found(request, exception):
    return HttpResponseNotFound("<h1>Page not found</h1><p>The pharmacy page you requested does not exist.</p>")