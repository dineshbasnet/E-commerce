from django import forms
from shop.models import Product, ProductImage

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ["name", "price", "description", "categories", "brand"]

class ProductImageForm(forms.ModelForm):
    class Meta:
        model = ProductImage
        fields = ["image"]
