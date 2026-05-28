from django.urls import path
from . import views

#app_name = 'pharmacy'

urlpatterns = [
    path('', views.index, name='home'),
    path('about/', views.about, name='about'),
    path('product/<slug:product_slug>/', views.show_product, name='product'),
    path('add/', views.add_product, name='add_product'),
    path('edit/<slug:product_slug>/', views.edit_product, name='edit_product'),
    path('contact/', views.contact, name='contact'),
    path('map/', views.map_view, name='map'),
    path('category/<slug:cat_slug>/', views.show_category, name='category'),
    path('tag/<slug:tag_slug>/', views.show_tag_products, name='tag'),
    path('chat/', views.cohere_chat, name='cohere_chat'),
    # legacy (optional)
    path('archive/<int:year>/', views.archive, name='archive'),
]