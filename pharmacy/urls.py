from django.urls import path
from pharmacy import views
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

admin.site.site_header = "Pharmacy Admin Panel"
admin.site.site_title = "Pharmacy Admin"
admin.site.index_title = "Welcome to Pharmacy Administration"

urlpatterns = [
    path('', views.index, name='home'),
    path('about/', views.about, name='about'),
    path('product/<slug:product_slug>/', views.show_product, name='product'),
    path('add/', views.add_product, name='add_product'),
    path('contact/', views.contact, name='contact'),
    path('category/<slug:cat_slug>/', views.show_category, name='category'),
    path('tag/<slug:tag_slug>/', views.show_tag_products, name='tag'),
    path('edit/<slug:product_slug>/', views.edit_product, name='edit_product'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)