from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Product, Category
from .forms import ProductForm

def product_list(request):
    query = request.GET.get('q')
    category_id = request.GET.get('category')

    products = Product.objects.filter(is_active=True)
    categories = Category.objects.all()

    if query:
        products = products.filter(title__icontains=query)

    if category_id:
        products = products.filter(category_id=category_id)

    return render(request, 'products/product_list.html', {
        'products': products,
        'categories': categories
    })

def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'products/product_detail.html', {'product': product})

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