from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseNotFound, JsonResponse
from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required, permission_required
from django.core.cache import cache
from django.conf import settings
from .models import Product, Category, Tag
from .forms import AddProductForm
from .services.cohere_service import CohereService
import json

# ===== Menu (fallback) =====
menu = [
    {'title': 'Home', 'url_name': 'home'},
    {'title': 'About', 'url_name': 'about'},
    {'title': 'Add Product', 'url_name': 'add_product'},
    {'title': 'Contact', 'url_name': 'contact'},
    {'title': '📍 Pharmacy Location', 'url_name': 'map'},
]


# ===== Index with search, pagination, caching =====
def index(request):
    # Base queryset (only published products)
    products_queryset = Product.published.all()

    # Search functionality
    search_query = request.GET.get('q', '').strip()
    if search_query:
        products_queryset = products_queryset.filter(
            name__icontains=search_query
        ) | products_queryset.filter(
            description__icontains=search_query
        )

    # Cache the count (optional, reduces DB hits)
    cache_key = f"product_count_{search_query}"
    total_products = cache.get(cache_key)
    if total_products is None:
        total_products = products_queryset.count()
        cache.set(cache_key, total_products, 60 * 5)  # 5 minutes

    # Pagination (6 products per page)
    paginator = Paginator(products_queryset, 6)
    page_number = request.GET.get('page')
    products = paginator.get_page(page_number)

    context = {
        'title': 'Pharmacy Home',
        'products': products,
        'search_query': search_query,
        'menu': menu,
    }
    return render(request, 'pharmacy/index.html', context)


# ===== Other views (unchanged except minor additions) =====
def about(request):
    return render(request, 'pharmacy/about.html', {'title': 'About Our Pharmacy', 'menu': menu})

def show_product(request, product_slug):
    product = get_object_or_404(Product, slug=product_slug, is_published=True)
    return render(request, 'pharmacy/product.html', {'product': product, 'menu': menu})

def show_category(request, cat_slug):
    category = get_object_or_404(Category, slug=cat_slug)
    products = Product.published.filter(category=category)
    paginator = Paginator(products, 6)
    page = request.GET.get('page')
    products_page = paginator.get_page(page)
    return render(request, 'pharmacy/index.html', {
        'products': products_page,
        'title': f'Category: {category.name}',
        'cat_selected': category.id,
        'menu': menu,
    })

def show_tag_products(request, tag_slug):
    tag = get_object_or_404(Tag, slug=tag_slug)
    products = tag.products.filter(is_published=True)
    paginator = Paginator(products, 6)
    page = request.GET.get('page')
    products_page = paginator.get_page(page)
    return render(request, 'pharmacy/index.html', {
        'products': products_page,
        'title': f'Tag: {tag.name}',
        'tag_selected': tag.slug,
        'menu': menu,
    })

@login_required
@permission_required('pharmacy.add_product', raise_exception=True)
def add_product(request):
    if request.method == 'POST':
        form = AddProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.author = request.user
            product.save()
            form.save_m2m()
            return redirect('home')
    else:
        form = AddProductForm()
    return render(request, 'pharmacy/add_product.html', {'form': form, 'menu': menu, 'title': 'Add Product'})

@login_required
@permission_required('pharmacy.change_product', raise_exception=True)
def edit_product(request, product_slug):
    product = get_object_or_404(Product, slug=product_slug)
    return HttpResponse(f"<h1>Edit Product</h1><p>Editing: {product.name}</p>")

def contact(request):
    context = {
        'title': 'Contact Us',
        'menu': menu,
        'google_maps_api_key': settings.GOOGLE_MAPS_API_KEY,
        'map_center_lat': 55.794182340233185,
        'map_center_lng': 49.14070131739104,
        'map_zoom': 16,
    }
    return render(request, 'pharmacy/contact.html', context)

def map_view(request):
    context = {
        'title': 'Pharmacy Location',
        'menu': menu,
        'google_maps_api_key': settings.GOOGLE_MAPS_API_KEY,
        'map_center_lat': 55.794182340233185,
        'map_center_lng': 49.14070131739104,
        'map_zoom': 14,
    }

    return render(request, 'pharmacy/map.html', context)

@csrf_exempt
@require_http_methods(["POST"])
def cohere_chat(request):
    try:
        data = json.loads(request.body)
        question = data.get('question', '')
        if not question.strip():
            return JsonResponse({'answer': 'Please enter a question.'})
        ai = CohereService()
        answer = ai.ask_question(question)
        return JsonResponse({'answer': answer})
    except Exception as e:
        print(f"Cohere chat error: {e}")
        return JsonResponse({'answer': 'AI service error. Try again later.'}, status=500)

# Legacy views (keep as needed)
def categories(request, cat_id):
    return HttpResponse(f"<h1>Medication Category</h1><p>Category ID: {cat_id}</p>")
def archive(request, year):
    if year > 2025:
        return redirect('home')
    return HttpResponse(f"<h1>Pharmacy Archive</h1><p>Year: {year}</p>")
def page_not_found(request, exception):
    return HttpResponseNotFound("<h1>Page not found</h1><p>The pharmacy page you requested does not exist.</p>")