from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required, permission_required
from django.conf import settings
from .models import Product, Category, Tag
from .forms import AddProductForm
from .services.mock_ai_service import MockAIService   # use mock AI (no API key needed)
import json

menu = [
    {'title': 'Home', 'url_name': 'home'},
    {'title': 'About', 'url_name': 'about'},
    {'title': 'Add Product', 'url_name': 'add_product'},
    {'title': 'Contact', 'url_name': 'contact'},
    {'title': '📍 Pharmacy Location', 'url_name': 'map'},
]

def index(request):
    products = Product.published.all()
    paginator = Paginator(products, 6)
    page = request.GET.get('page')
    products_page = paginator.get_page(page)
    return render(request, 'pharmacy/index.html', {
        'title': 'Pharmacy Home',
        'products': products_page,
        'menu': menu,
    })

def about(request):
    return render(request, 'pharmacy/about.html', {'title': 'About Us', 'menu': menu})

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
        'map_center_lat': 55.751574,
        'map_center_lng': 37.573856,
        'map_zoom': 16,
    }
    return render(request, 'pharmacy/contact.html', context)

def map_view(request):
    context = {
        'title': 'Pharmacy Location',
        'menu': menu,
        'google_maps_api_key': settings.GOOGLE_MAPS_API_KEY,
        'map_center_lat': 55.751574,
        'map_center_lng': 37.573856,
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
        ai = MockAIService()
        answer = ai.ask_question(question)
        return JsonResponse({'answer': answer})
    except Exception as e:
        return JsonResponse({'answer': 'AI service error. Try again later.'}, status=500)

def archive(request, year):
    if year > 2025:
        return redirect('home')
    return HttpResponse(f"<h1>Archive</h1><p>Year: {year}</p>")