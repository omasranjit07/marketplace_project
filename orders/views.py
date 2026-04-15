import stripe
from django.conf import settings
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from cart.models import CartItem
from .models import Order, OrderItem

def stripe_checkout(request):
    cart_items = CartItem.objects.filter(user=request.user)
    line_items = []
    for item in cart_items:
        line_items.append({
            'price_data': {
                'currency': 'usd',
                'product_data': {
                    'name': item.product.title,
                },
                'unit_amount': int(item.product.price * 100),
            },
            'quantity': item.quantity,
        })
    
    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=line_items,
        mode='payment',
        success_url=request.build_absolute_uri(reverse("payment_success"))
        + "?session_id={CHECKOUT_SESSION_ID}",
        cancel_url=request.build_absolute_uri(reverse("cart_detail")),
    )
 
    if session.url:
        return redirect(session.url)
    else:
        return redirect('cart_detail')