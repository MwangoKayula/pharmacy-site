from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from pharmacy import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name='home'),
    path('about/', views.about, name='about'),
    path('product/<slug:product_slug>/', views.show_product, name='product'),
    path('category/<slug:cat_slug>/', views.show_category, name='category'),

    path('admin/', admin.site.urls),
    path('pharmacy/', include('pharmacy.urls')),          # all pharmacy URLs under /pharmacy/
    path('', RedirectView.as_view(url='/pharmacy/', permanent=False)),  # redirect root to /pharmacy/

    path('tag/<slug:tag_slug>/', views.show_tag_products, name='tag'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)