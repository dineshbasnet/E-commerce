from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from shop.models import Product, Category, Brand, ProductImage
from vendor.forms import ProductForm
from django.http import HttpResponse

def vendor_required(view_func):
    """Decorator to restrict access to vendors only"""
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated or request.user.user_type != 'vendor':
            messages.error(request, "You must be a vendor to access this page.")
            return redirect("home")  # Redirect to homepage or login page
        return view_func(request, *args, **kwargs)
    return wrapper

@login_required
@vendor_required
def vendor_products(request):
    """List all products added by the logged-in vendor"""
    products = Product.objects.filter(vendor=request.user)
    return render(request, "vendor/vendor_products.html", {"products": products})

@login_required
@vendor_required
def add_product(request):
    """Allow vendors to add new products"""
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            # Save the product first
            product = form.save(commit=False)
            product.vendor = request.user  # Assign logged-in user as vendor
            product.save()

            # Now handle the image uploads (if any)
            images = request.FILES.getlist('images')  # 'images' is the name attribute for the file input
            for image in images:
                ProductImage.objects.create(product=product, image=image)

            messages.success(request, "Product added successfully!")
            return redirect("vendor_products")
    else:
        form = ProductForm()

    return render(request, "vendor/add_product.html", {"form": form})

@login_required
@vendor_required
def edit_product(request, product_id):
    """Allow vendors to edit their products"""
    product = get_object_or_404(Product, id=product_id, vendor=request.user)
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()

            # Handle image updates (if any new images are uploaded)
            if 'images' in request.FILES:
                images = request.FILES.getlist('images')
                for image in images:
                    ProductImage.objects.create(product=product, image=image)

            messages.success(request, "Product updated successfully!")
            return redirect("vendor_products")
    else:
        form = ProductForm(instance=product)

    return render(request, "vendor/edit_product.html", {"form": form, "product": product})

@login_required
@vendor_required
def delete_product(request, product_id):
    """Allow vendors to delete their products"""
    product = get_object_or_404(Product, id=product_id, vendor=request.user)
    if request.method == "POST":
        product.delete()
        messages.success(request, "Product deleted successfully!")
        return redirect("vendor_products")
    return render(request, "vendor/delete_product.html", {"product": product})
