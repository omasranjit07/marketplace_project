from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Product, Category, Review
from .forms import ProductForm, ReviewForm
from django.core.paginator import Paginator
from django.http import HttpResponseForbidden

def product_list(request):
    products = Product.objects.all()

    paginator = Paginator(products, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'products/product_list.html', {
        'page_obj': page_obj
    })

def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'products/product_detail.html', {'product': product})

@login_required
def add_review(request, pk):
    product = get_object_or_404(Product, pk=pk)

    if request.method == 'POST':
        Review.objects.create(
            product=product,
            user=request.user,
            rating=request.POST.get('rating'),
            comment=request.POST.get('comment')
        )

    return redirect('product_detail', pk=pk)

@login_required
def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.seller = request.user
            product.save()
            return redirect('product_list')
    else:
        form = ProductForm()

    return render(request, 'products/add_product.html', {'form': form})

@login_required
def my_products(request):
    products = Product.objects.filter(seller=request.user)
    return render(request, 'products/my_products.html', {'products': products})

@login_required
def edit_product(request, pk):
    product = get_object_or_404(Product, pk=pk)

    if product.seller != request.user:
        return HttpResponseForbidden("You are not allowed")

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('my_products')
    else:
        form = ProductForm(instance=product)

    return render(request, 'products/edit_product.html', {'form': form})


@login_required
def delete_product(request, pk):
    product = get_object_or_404(Product, pk=pk)

    if product.seller != request.user:
        return HttpResponseForbidden("You are not allowed")

    product.delete()
    return redirect('my_products')