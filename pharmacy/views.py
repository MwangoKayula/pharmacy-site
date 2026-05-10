from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.urls import reverse
from django.utils.text import slugify
from .forms import UploadFileForm
from .models import Product, Category, Tag
from .forms import AddProductForm
import uuid
import os


def handle_uploaded_file(f):
    # Get file extension
    name, ext = os.path.splitext(f.name)
    # Generate unique name
    unique_name = f"{name}_{uuid.uuid4().hex}{ext}"
    # Ensure the upload directory exists
    upload_dir = os.path.join('media', 'uploads')
    os.makedirs(upload_dir, exist_ok=True)
    # Save file
    file_path = os.path.join(upload_dir, unique_name)
    with open(file_path, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
    return unique_name  # return the saved filename

def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file = request.FILES['file']
            filename = handle_uploaded_file(uploaded_file)
            return render(request, 'pharmacy/upload_success.html', {
                'filename': filename,
                'menu': menu,
                'title': 'Upload Success'
            })
    else:
        form = UploadFileForm()
    context = {
        'title': 'Upload Prescription',
        'menu': menu,
        'form': form,
    }
    return render(request, 'pharmacy/upload.html', context)

# Menu definition (used in all views)
menu = [
    {'title': 'Home', 'url_name': 'home'},
    {'title': 'About', 'url_name': 'about'},
    {'title': 'Add Product', 'url_name': 'add_product'},   # this is the link to /add/
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
        form = AddProductForm(request.POST, request.FILES)   # handles both text and file
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = AddProductForm()
    context = {
        'title': 'Add Product',
        'menu': menu,   # make sure 'menu' is defined in this view
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