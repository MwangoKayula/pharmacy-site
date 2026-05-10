import re
from django import forms
from django.core.exceptions import ValidationError
from .models import Product, Category, Tag

class AddProductForm(forms.ModelForm):
    # Override category and tags to customise appearance
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        empty_label="-- Select category --",
        label="Category",
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        required=False,
        label="Tags",
        widget=forms.SelectMultiple(attrs={'class': 'form-select'})
    )

    class Meta:
        model = Product
        # Include ALL fields you want to show, including image
        fields = ['name', 'slug', 'description', 'price', 'is_published', 'category', 'tags', 'image']
        labels = {
            'name': 'Product name',
            'slug': 'URL slug',
            'description': 'Description',
            'price': 'Price ($)',
            'is_published': 'Published',
            'image': 'Product image',
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'e.g., Paracetamol 500mg'}),
            'slug': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'auto-generated from name'}),
            'description': forms.Textarea(attrs={'class': 'form-textarea', 'rows': 4}),
            'price': forms.NumberInput(attrs={'class': 'form-input', 'step': '0.01', 'placeholder': '0.00'}),
            'is_published': forms.CheckboxInput(attrs={'class': 'form-checkbox'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-input'}),
        }

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if len(name) > 100:
            raise ValidationError('Product name cannot exceed 100 characters.')
        return name

# Optional: separate form for generic file upload (if needed for Work 48)
class UploadFileForm(forms.Form):
    file = forms.FileField(label="Select a file")