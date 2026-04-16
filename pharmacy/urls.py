from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from pharmacy import views

urlpatterns = [
    path('', views.index, name='home'),
    path('about/', views.about, name='about'),
    #path('product/<int:product_id>/', views.show_product, name='product'),
    path('product/<slug:product_slug>/', views.show_product, name='product'),
    path('add/', views.add_product, name='add_product'),
    path('contact/', views.contact, name='contact'),
    path('login/', views.login, name='login'),
    path('category/<int:cat_id>/', views.show_category, name='category'),
]