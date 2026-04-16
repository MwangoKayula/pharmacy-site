from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.shortcuts import redirect
from django.urls import reverse
from django.shortcuts import render 
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from .models import Product

categories_db = [
    {'id': 1, 'name': 'Pain Relief'},
    {'id': 2, 'name': 'Antibiotics'},
    {'id': 3, 'name': 'Vitamins & Supplements'},
    {'id': 4, 'name': 'First Aid'},
]

menu = [
    {'title': 'Home', 'url_name': 'home'},
    {'title': 'About', 'url_name': 'about'},
    {'title': 'Add Product', 'url_name': 'add_product'},
    {'title': 'Contact', 'url_name': 'contact'},
    {'title': 'Login', 'url_name': 'login'},
]

def show_product(request, product_slug):
    product = get_object_or_404(Product, slug=product_slug, is_published=True)
    context = {
        'title': product.name,
        'menu': menu,
        'product': product,
    }
    return render(request, 'pharmacy/product.html', context)

def show_product(request, product_id):
    return HttpResponse(f"<h1>Product Details</h1><p>Showing product with ID: {product_id}</p>")

def add_product(request):
    return HttpResponse("<h1>Add New Product</h1><p>Form will go here.</p>")

def contact(request):
    return HttpResponse("<h1>Contact Us</h1><p>Email: pharmacy@example.com</p>")

def login(request):
    return HttpResponse("<h1>Login</h1><p>Please log in.</p>")


class Medication:
    def __init__(self, name, price):
        self.name = name
        self.price = price

products_db = [
    {'id': 1, 'name': 'Paracetamol 500mg', 'description': 'Pain reliever and fever reducer.', 'is_published': True},
    {'id': 2, 'name': 'Ibuprofen 400mg', 'description': 'Anti‑inflammatory pain relief.', 'is_published': False},
    {'id': 3, 'name': 'Amoxicillin 250mg', 'description': 'Antibiotic for bacterial infections.', 'is_published': True},
    {'id': 4, 'name': 'Vitamin D3 1000 IU', 'description': 'Supports bone health.', 'is_published': True},
]

def index(request):
    print("Menu:", menu)   # temporary debug
    context = { ... }
    
def index(request):
    products = Product.published.all()   # only published
    context = {
        'title': 'Pharmacy Home',
        'menu': menu,
        'products': products,
    }
    return render(request, 'pharmacy/index.html', context)

def about(request):
    context = {
        'title': 'About Our Pharmacy',
        'menu': menu,
    }
    return render(request, 'pharmacy/about.html', context)


def categories(request, cat_id):
    return HttpResponse(f"<h1>Medication Category</h1><p>Category ID: {cat_id}</p>")


def show_category(request, cat_id):
    """
    Temporary placeholder for category filtering.
    Later you will filter products by cat_id.
    """
    # For now, just display all products (same as index)
    context = {
        'title': f'Category {cat_id}',
        'menu': menu,
        'products': products_db,
        'cat_selected': cat_id,   # optional, for highlighting
    }
    return render(request, 'pharmacy/index.html', context)

def categories_by_slug(request, cat_slug):
    if request.GET:
        print("GET parameters:", request.GET)
    return HttpResponse(f"<h1>Medication Category</h1><p>Slug: {cat_slug}</p>")

# Archive view with redirect logic
def archive(request, year):
    if year > 2025:
        # Redirect to home page (or any named URL)
        return redirect('home')          # temporary redirect (302)
        # or permanent: return redirect('home', permanent=True)
    return HttpResponse(f"<h1>Pharmacy Archive</h1><p>Year: {year}</p>")

# Custom 404 page
def page_not_found(request, exception):
    return HttpResponseNotFound("<h1>Page not found</h1><p>The pharmacy page you requested does not exist.</p>")