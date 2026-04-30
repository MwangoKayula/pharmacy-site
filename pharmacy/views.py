from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.urls import reverse
from django.utils.text import slugify

from .models import Product, Category, Tag
from .forms import AddProductForm


# Menu definition (used in all views)
menu = [
    {'title': 'Home', 'url_name': 'home'},
    {'title': 'About', 'url_name': 'about'},
    {'title': 'Add Product', 'url_name': 'add_product'},
    {'title': 'Contact', 'url_name': 'contact'},
    {'title': 'Login', 'url_name': 'login'},
]


# ---------- Main views ----------
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


def show_tag_products(request, tag_slug):
    tag = get_object_or_404(Tag, slug=tag_slug)
    products = tag.products.filter(is_published=True)
    context = {
        'title': f'Tag: {tag.name}',
        'menu': menu,
        'products': products,
        'tag_selected': tag.slug,
    }
    return render(request, 'pharmacy/index.html', context)


# ---------- Form handling ----------
def add_product(request):
    if request.method == 'POST':
        form = AddProductForm(request.POST)
        if form.is_valid():
            cleaned_data = form.cleaned_data

            # Generate slug if not provided
            slug = cleaned_data.get('slug')
            if not slug:
                slug = slugify(cleaned_data['name'])

            # Ensure unique slug
            original_slug = slug
            counter = 1
            while Product.objects.filter(slug=slug).exists():
                slug = f"{original_slug}-{counter}"
                counter += 1

            # Create product (without many-to-many tags first)
            try:
                product = Product.objects.create(
                    name=cleaned_data['name'],
                    slug=slug,
                    description=cleaned_data['description'],
                    price=cleaned_data['price'],
                    is_published=cleaned_data['is_published'],
                    category=cleaned_data['category']
                )
                # Add tags (many-to-many)
                product.tags.set(cleaned_data['tags'])
                # Redirect to home on success
                return redirect('home')
            except Exception as e:
                form.add_error(None, f"Database error: {str(e)}")
        # If form is invalid or save fails, fall through to re-render with errors
    else:
        form = AddProductForm()

    context = {
        'title': 'Add Product',
        'menu': menu,
        'form': form,
    }
    return render(request, 'pharmacy/add_product.html', context)


# ---------- Placeholders for other menu items ----------
def contact(request):
    return HttpResponse("<h1>Contact Us</h1><p>Email: pharmacy@example.com</p>")


def login(request):
    return HttpResponse("<h1>Login</h1><p>Please log in.</p>")


# ---------- Archive and error handling (from earlier works) ----------
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


# ---------- Custom manager demonstration (not used in frontend, kept for reference) ----------
# The PublishedManager is defined in models.py and used as Product.published