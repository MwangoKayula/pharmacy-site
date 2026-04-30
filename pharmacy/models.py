from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.urls import reverse

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

    def get_absolute_url(self):
        return reverse('category', kwargs={'cat_slug': self.slug})

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('category', kwargs={'cat_slug': self.slug})

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
    slug = models.SlugField(max_length=100, unique=True, db_index=True, verbose_name="URL Slug")
    description = models.TextField(blank=True, verbose_name="Description")
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, verbose_name="Price")
    is_published = models.BooleanField(default=True, verbose_name="Published")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated")
    category = models.ForeignKey(Category, on_delete=models.PROTECT, null=True, blank=True, verbose_name="Category")

    tags = models.ManyToManyField(Tag, blank=True, related_name='products')

    # Managers
    objects = models.Manager()
    published = PublishedManager()

    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = 'Products'
        ordering = ['-created_at']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('product', kwargs={'product_slug': self.slug})