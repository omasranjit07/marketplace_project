from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import CartItem
from products.models import Product

@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    if product.stock < 1:
        return redirect('product_list')

    cart_item, created = CartItem.objects.get_or_create(user=request.user, product=product)

    if not created and cart_item.quantity < product.stock:
        cart_item.quantity += 1
        cart_item.save()

    return redirect('cart_detail')


@login_required
def cart_detail(request):
    items = CartItem.objects.filter(user=request.user)
    total = sum(item.product.price * item.quantity for item in items)

    return render(request, 'cart/cart_detail.html', {
        'items': items,
        'total': total,
    })


@login_required
def remove_from_cart(request, item_id):
    item = get_object_or_404(CartItem, id=item_id, user=request.user)
    item.delete()
    return redirect('cart_detail')
