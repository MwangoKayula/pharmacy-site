from django.urls import path
from pharmacy import views

urlpatterns = [
    path('', views.index, name='home'),
    path('about/', views.about, name='about'),
    path('product/<slug:product_slug>/', views.show_product, name='product'),
    path('add/', views.add_product, name='add_product'),
    path('contact/', views.contact, name='contact'),
    path('login/', views.login, name='login'),
    path('category/<slug:cat_slug>/', views.show_category, name='category'),
]