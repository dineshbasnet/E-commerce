from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from shop.models import Product
from .models import CartProduct, Cart, State, District, Municipality, DeliveryAddress, Order
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404




@login_required(login_url='login_view')
@require_POST
def place_order(request):
    delivery_address_id = request.POST.get('delivery-address')
    payment_method = request.POST.get('payment-method')
    product_id = request.POST.get('product-id')
    
    try:
        address = DeliveryAddress.objects.get(id=delivery_address_id)
        cart_product = CartProduct.objects.get(id=product_id)
    except DeliveryAddress.DoesNotExist:
        return redirect("cart_view")
    else:
        try:
            order = Order.objects.create(
                product=cart_product,
                delivery_address=address,
                payment_method=payment_method
            ) 
        except Exception as e:
            print(e) 
        else:
            cart_product.ordered = True
            cart_product.save()
        finally:
            return redirect("cart_view")   


@login_required


def get_districts(request):
    state_id = request.GET.get('state_id')
    if not state_id:
        return JsonResponse({'error': 'Missing state_id'}, status=400)

    districts = District.objects.filter(state_id=state_id).values('id', 'name')
    return JsonResponse(list(districts), safe=False)


def get_municipalities(request):
    district_id = request.GET.get('district_id')
    if district_id:
        municipalities = Municipality.objects.filter(district__id=district_id).values("id", "name")

        return JsonResponse(list(municipalities), safe=False)
    return JsonResponse([], safe=False)

@require_POST
@login_required(login_url='login_view')
def add_delivery_address(request):
    """Handles adding delivery address"""
    state_id = request.POST.get('state-id')
    district_id = request.POST.get('district-id')
    municipality_id = request.POST.get('municipality-id')
    local_address = request.POST.get('local-address')
    cart_product_id = request.POST.get('cart_product_id')

    try:
        state = get_object_or_404(State, id=state_id)
        district = get_object_or_404(District, id=district_id, state=state)
        municipality = get_object_or_404(Municipality, id=municipality_id, district=district)

        DeliveryAddress.objects.create(
            user=request.user,
            state=state,
            district=district,
            municipality=municipality,
            local_address=local_address
        )
        return redirect("checkout", cart_product_id=cart_product_id)
    except Exception as e:
        print(e)
        return redirect("checkout", cart_product_id=cart_product_id)

        

@login_required(login_url='login_view')
def checkout(request, cart_product_id):
    try:
        cart_product = CartProduct.objects.get(id=cart_product_id)
    except CartProduct.DoesNotExist:
        return redirect("cart_view")

    if request.method == 'POST':
        quantity = request.POST.get('quantity')
        print(f"Received quantity: {quantity}")  # Debugging line
        if quantity:
            try:
                new_quantity = int(quantity)
                if new_quantity < 1:
                    new_quantity = 1  # Prevent negative or zero quantity
                cart_product.quantity = new_quantity
                cart_product.save()  # Save the updated quantity
                print(f"Updated quantity to: {cart_product.quantity}")  # Debugging line
            except ValueError:
                print("Invalid quantity value")  # Handle invalid input
            except Exception as e:
                print(f"Error saving quantity: {e}")  # Log any errors

    # Prepare context for rendering the checkout page
    states = State.objects.all()
    districts = District.objects.all()
    municipalities = Municipality.objects.all()
    delivery_addresses = DeliveryAddress.objects.filter(user=request.user)

    context = {
        'product': cart_product,
        'states': states,
        'districts': districts,
        'municipalities': municipalities,
        'delivery_addresses': delivery_addresses
    }
    return render(request, "cart/product_checkout.html", context)

@login_required(login_url='login_view')
@require_POST
def update_cart_quantity(request, cart_product_id):
    """AJAX view to update the quantity of a cart product."""
    try:
        cart_product = CartProduct.objects.get(id=cart_product_id)
        quantity = request.POST.get('quantity')
        if quantity:
            new_quantity = int(quantity)
            if new_quantity < 1:
                new_quantity = 1  # Prevent negative or zero quantity
            cart_product.quantity = new_quantity
            cart_product.save()
            return JsonResponse({'success': True, 'quantity': cart_product.quantity})
    except CartProduct.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Cart product not found.'})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})

@login_required(login_url='login_view')
def delete_product_from_cart(request, cart_product_id):
    if request.method == "POST":
        cart_product_id = request.POST.get("product_id", None)
        if cart_product_id is not None:
            try:
                cart_product = CartProduct.objects.get(id=cart_product_id)
            except CartProduct.DoesNotExist:
                return redirect("cart_view")
            else:
                cart_product.delete()
                return redirect("cart_view")

    try:
        cart_product = CartProduct.objects.get(id=cart_product_id)
    except CartProduct.DoesNotExist:
        print("cart product not exist")
        return redirect("cart_view")
    else:
        context = {
            'product': cart_product
        }
        return render(request, "cart/cart_product_delete.html", context)

@login_required(login_url='login_view')
def cart_view(request):
    try:
        cart = Cart.objects.get(user=request.user)
        cart_products = CartProduct.objects.select_related('product').filter(cart=cart, ordered=False)  
    except Exception as e:
        print(e)
        return redirect('shop_view')   
    else:
        context = {
            'products': cart_products
        }
        return render(request, 'cart/cart.html', context)

@login_required(login_url='login_view')
def add_to_cart_view(request, product_id):
    try:
        product = Product.objects.get(id=product_id)
        cart = Cart.objects.get(user=request.user)
    except Product.DoesNotExist:
        return redirect('shop_view')
    except Cart.DoesNotExist:
        return redirect('shop_view')
    except Exception as e:
        print(e)
        return redirect('shop_view')
    else:
        try:
            CartProduct.objects.create(
                cart=cart,
                product=product,
            )
        except Exception as e:
            print(e)
            return redirect('shop_view')
        else:
            return redirect('cart_view')