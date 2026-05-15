from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.conf import settings 

# Custom manager for published products
class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_published=True)

# Category model
class Category(models.Model):
    name = models.CharField(max_length=100, db_index=True, verbose_name="Category Name")
    slug = models.SlugField(max_length=100, unique=True, db_index=True, verbose_name="URL Slug")

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
        ordering = ['name']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('category', kwargs={'cat_slug': self.slug})

# Tag model
class Tag(models.Model):
    name = models.CharField(max_length=100, db_index=True, verbose_name="Tag Name")
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL Slug")

    class Meta:
        verbose_name = 'Tag'
        verbose_name_plural = 'Tags'
        ordering = ['name']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('tag', kwargs={'tag_slug': self.slug})

# Product model
class Product(models.Model):
    name = models.CharField(max_length=100, verbose_name="Product Name")
    slug = models.SlugField(max_length=100, unique=True, db_index=True, blank=True)
    description = models.TextField(blank=True, verbose_name="Description")
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, verbose_name="Price")
    is_published = models.BooleanField(default=True, verbose_name="Published")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated")
    category = models.ForeignKey(Category, on_delete=models.PROTECT, null=True, blank=True, verbose_name="Category")
    tags = models.ManyToManyField(Tag, blank=True, related_name='products')
    image = models.ImageField(upload_to='products/%Y/%m/%d/', blank=True, null=True, verbose_name="Product image")

    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='products',
        verbose_name="Author"
    )

    # Managers
    objects = models.Manager()
    published = PublishedManager()

    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = 'Products'
        ordering = ['-created_at']   # newest first

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('product', kwargs={'product_slug': self.slug})

    def save(self, *args, **kwargs):
        # Generate slug if empty
        if not self.slug:
            base_slug = slugify(self.name)
            slug = base_slug
            counter = 1
            # Ensure uniqueness
            while Product.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)