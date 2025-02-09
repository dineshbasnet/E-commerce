from django.shortcuts import render, redirect
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import CustomUser
from cart.models import Cart


def logout_view(request):
    logout(request)
    return redirect('login_view')


def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        if not email or not password:
            return render(request, 'account/login.html', {'error': 'All fields are required'})

        user = authenticate(request, email=email.lower().strip(), password=password)  # Normalize email
        if user is not None:
            login(request, user)

            # Redirect vendors to the vendor dashboard
            if user.user_type == 'vendor':
                return redirect('vendor_products')  # Change this to your vendor dashboard URL
            
            return redirect('shop_view')

        return render(request, 'account/login.html', {'error': 'Invalid credentials'})

    return render(request, 'account/login.html')


def register(request):
    if request.method == 'POST':
        email = request.POST.get('email').lower().strip()  # Normalize email
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        user_type = request.POST.get('user_type')

        if not email or not password or not confirm_password or not user_type:
            return render(request, 'account/register.html', {'error': 'All fields are required'})

        if password != confirm_password:
            return render(request, 'account/register.html', {'error': 'Passwords do not match'})

        if CustomUser.objects.filter(email=email).exists():
            return render(request, 'account/register.html', {'error': 'This email is already in use. Please try another.'})

        try:
            validate_password(password)
        except Exception as e:
            return render(request, 'account/register.html', {'errors': list(e)})

        try:
            new_user = CustomUser.objects.create_user(email=email, password=password, user_type=user_type)

            if user_type == 'customer':
                Cart.objects.create(user=new_user)  # Create cart for customers

        except Exception as e:
            return render(request, 'account/register.html', {'error': str(e)})

        messages.success(request, "Account created successfully. You can now log in.")

        # Redirect vendors to their dashboard after registration
        if user_type == 'vendor':
            return redirect('vendor_products')  # Update this with the correct vendor dashboard URL

        return redirect('login_view')

    return render(request, 'account/register.html')
