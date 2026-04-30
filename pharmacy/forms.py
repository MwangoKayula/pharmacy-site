from django import forms
from .models import Category, Tag

class AddProductForm(forms.Form):
    name = forms.CharField(
        max_length=100,
        label="Product name",
        widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'e.g., Paracetamol 500mg'})
    )
    slug = forms.SlugField(
        max_length=100,
        label="URL slug",
        widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'auto-generated from name'})
    )
    description = forms.CharField(
        widget=forms.Textarea(attrs={'cols': 50, 'rows': 5, 'class': 'form-textarea'}),
        required=False,
        label="Description"
    )
    price = forms.DecimalField(
        max_digits=10,
        decimal_places=2,
        label="Price ($)",
        widget=forms.NumberInput(attrs={'class': 'form-input', 'step': '0.01'})
    )
    is_published = forms.BooleanField(
        required=False,
        label="Published",
        initial=True,
        widget=forms.CheckboxInput(attrs={'class': 'form-checkbox'})
    )
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        label="Category",
        empty_label="-- Select category --",
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        required=False,
        label="Tags",
        widget=forms.SelectMultiple(attrs={'class': 'form-select'})
    )