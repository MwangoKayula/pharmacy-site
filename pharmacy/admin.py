from django.contrib import admin
from django.utils.html import format_html
from .models import Product, Category, Tag


# Custom price range filter (for list view)
class PriceRangeFilter(admin.SimpleListFilter):
    title = "Price range"
    parameter_name = "price_range"

    def lookups(self, request, model_admin):
        return [
            ('cheap', 'Under $10'),
            ('medium', '$10 - $20'),
            ('expensive', 'Over $20'),
        ]

    def queryset(self, request, queryset):
        if self.value() == 'cheap':
            return queryset.filter(price__lt=10)
        if self.value() == 'medium':
            return queryset.filter(price__gte=10, price__lte=20)
        if self.value() == 'expensive':
            return queryset.filter(price__gt=20)
        return queryset

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'is_published', 'category', 'image_preview', 'created_at')
    list_display_links = ('name',)
    list_editable = ('is_published', 'price')
    ordering = ('-created_at', 'name')
    search_fields = ('name', 'description', 'category__name')
    list_filter = ('is_published', 'category', 'tags')
    list_per_page = 5
    prepopulated_fields = {'slug': ('name',)}
    fields = ('name', 'slug', 'description', 'price', 'is_published', 'category', 'tags', 'image')
    readonly_fields = ('created_at', 'updated_at')
    actions = ['publish_products', 'unpublish_products']

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-height: 50px; max-width: 50px;" />', obj.image.url)
        return "-"
    image_preview.short_description = 'Image Preview'

    # ---------- Custom methods ----------
    @admin.display(description="Description length (chars)")
    def desc_length(self, obj):
        return len(obj.description) if obj.description else 0

    @admin.action(description="Publish selected products")
    def publish_products(self, request, queryset):
        count = queryset.update(is_published=True)
        self.message_user(request, f"{count} product(s) have been published.")

    @admin.action(description="Unpublish selected products")
    def unpublish_products(self, request, queryset):
        count = queryset.update(is_published=False)
        self.message_user(request, f"{count} product(s) have been unpublished.", level='WARNING')


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug')
    list_display_links = ('id', 'name')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}
    ordering = ('name',)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug')
    list_display_links = ('id', 'name')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}
    ordering = ('name',)