from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from cart.models import CartItem
from .models import Order, OrderItem

@login_required
def checkout(request):
    cart_items = CartItem.objects.filter(user=request.user)

    if not cart_items.exists():
        return redirect('cart_detail')

    total = sum(item.product.price * item.quantity for item in cart_items)

    order = Order.objects.create(
        user=request.user,
        total_amount=total,
        status='Placed'
    )

    for item in cart_items:
        OrderItem.objects.create(
            order=order,
            product=item.product,
            quantity=item.quantity,
            price=item.product.price
        )
    
    for item in cart_items:
        if item.quantity > item.product.stock:
            return redirect('cart_detail')

        item.product.stock -= item.quantity
        item.product.save()

    cart_items.delete()

    return render(request, 'orders/order_success.html', {'order': order})

@login_required
def order_history(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'orders/order_history.html', {'orders': orders})