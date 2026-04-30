from django.contrib import admin
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
    # ---------- List display customisation (Work 38, 39, 40) ----------
    list_display = ('name', 'price', 'is_published', 'category', 'created_at', 'desc_length')
    list_display_links = ('name',)
    list_editable = ('is_published', 'price')
    ordering = ('-created_at', 'name')
    search_fields = ('name', 'description', 'category__name')
    list_filter = ('is_published', 'category', 'tags', PriceRangeFilter)
    list_per_page = 5
    actions = ['publish_products', 'unpublish_products']

    # ---------- Form editing (Work 41) ----------
    # Order of fields in the add/edit form
    fields = ['name', 'slug', 'description', 'price', 'is_published', 'category', 'tags']
    # Automatically generate slug from the name field (client-side)
    prepopulated_fields = {'slug': ('name',)}
    # Improve many-to-many widget for tags
    filter_horizontal = ['tags']

    # ---------- Other settings ----------
    # Prepopulated slug may be overridden if we also want readonly, but prepopulated takes precedence
    readonly_fields = ('created_at', 'updated_at')   # these are not in 'fields', so they won't appear on edit form anyway

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