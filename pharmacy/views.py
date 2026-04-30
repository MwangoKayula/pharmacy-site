from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Product, Category
from django.utils.text import slugify
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
    if request.method == 'POST':
        # Get data from the form
        name = request.POST.get('name')
        price = request.POST.get('price')
        description = request.POST.get('description')
        category_id = request.POST.get('category')
        is_published = request.POST.get('is_published') == 'on'

        # Basic validation
        if name and price:
            # Create slug from name
            slug = slugify(name)
            # Ensure unique slug (simple approach)
            original_slug = slug
            counter = 1
            while Product.objects.filter(slug=slug).exists():
                slug = f"{original_slug}-{counter}"
                counter += 1

            # Get category (if selected)
            category = None
            if category_id:
                try:
                    category = Category.objects.get(id=category_id)
                except Category.DoesNotExist:
                    pass

            # Create product
            Product.objects.create(
                name=name,
                slug=slug,
                price=price,
                description=description,
                category=category,
                is_published=is_published
            )
            # Show success message and clear form? Or redirect
            context = {
                'title': 'Add Product',
                'menu': menu,
                'categories': Category.objects.all(),
                'message': f'Product "{name}" added successfully!'
            }
            return render(request, 'pharmacy/add_product.html', context)
        else:
            context = {
                'title': 'Add Product',
                'menu': menu,
                'categories': Category.objects.all(),
                'error': 'Name and price are required.'
            }
            return render(request, 'pharmacy/add_product.html', context)
    else:
        # GET request – just show empty form
        context = {
            'title': 'Add Product',
            'menu': menu,
            'categories': Category.objects.all(),
        }
        return render(request, 'pharmacy/add_product.html', context)

def contact(request):
    return HttpResponse("<h1>Contact Us</h1><p>Email: pharmacy@example.com</p>")

def login(request):
    return HttpResponse("<h1>Login</h1><p>Please log in.</p>")