import stripe
from django.conf import settings
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from cart.models import CartItem
from .models import Order, OrderItem

stripe.api_key = settings.STRIPE_SECRET_KEY

@login_required
def stripe_checkout(request):
    cart_items = CartItem.objects.filter(user=request.user)

    if not cart_items.exists():
        return redirect('cart_detail')

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

        # 👇 IMPORTANT: pass session_id back
        success_url='http://127.0.0.1:8000/orders/success/?session_id={CHECKOUT_SESSION_ID}',
        cancel_url='http://127.0.0.1:8000/cart/',
    )

    return redirect(session.url)

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

@login_required
def order_detail(request, pk):
    order = get_object_or_404(Order, pk=pk, user=request.user)
    return render(request, 'orders/order_detail.html', {'order': order})

@login_required
def payment_success(request):
    session_id = request.GET.get('session_id')

    if not session_id:
        return redirect('cart_detail')

    try:
        session = stripe.checkout.Session.retrieve(session_id)
    except Exception:
        return redirect('cart_detail')

    # Verify payment
    if session.payment_status != 'paid':
        return redirect('cart_detail')

    user = request.user
    cart_items = CartItem.objects.filter(user=user)

    if not cart_items.exists():
        return redirect('product_list')

    # Prevent duplicate orders
    if Order.objects.filter(stripe_session_id=session_id).exists():
        return redirect('product_list')

    total = sum(item.product.price * item.quantity for item in cart_items)

    order = Order.objects.create(
        user=user,
        total_amount=total,
        status='Placed',
        stripe_session_id=session_id
    )

    for item in cart_items:
        OrderItem.objects.create(
            order=order,
            product=item.product,
            quantity=item.quantity,
            price=item.product.price
        )

        item.product.stock -= item.quantity
        item.product.save()

    cart_items.delete()

    return render(request, 'orders/payment_success.html', {'order': order})