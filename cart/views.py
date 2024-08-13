from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Cart, CartItem
from products.models import Product
from django.contrib import messages

@login_required
def cart_detail(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_items = cart.items.all()
    total = sum(item.product.price * item.quantity for item in cart_items)
    return render(request, 'cart/cart_details.html', {'cart_items': cart_items, 'total': total})


@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart, created = Cart.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))
        
        if quantity < 1:
            messages.error(request, "Quantity must be at least 1.")
            return redirect('product_detail', product_id=product.id)
        
        if quantity > product.stock:
            messages.error(request, f"Sorry, we only have {product.stock} in stock.")
            return redirect('product_detail', product_id=product.id)

        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
        
        if created:
            cart_item.quantity = quantity
        else:
            cart_item.quantity += quantity
        
  
        cart_item.save()
        product.save()
        messages.success(request, f"Added {quantity} {product.name} to your cart.")
    return  HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


from django.views.decorators.http import require_POST
@login_required
def update_cart_item(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    action = request.POST.get('action')

    if action == 'increase':
        cart_item.quantity += 1
    elif action == 'decrease':
        cart_item.quantity = max(1, cart_item.quantity - 1)
    elif action == 'remove':
        cart_item.delete()
        messages.success(request, f"{cart_item.product.name} removed from your cart.")
        return redirect('cart_detail')

    cart_item.save()
    messages.success(request, "Cart updated successfully.")
    return redirect('cart_detail')

