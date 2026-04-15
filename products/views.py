from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Product, Category, Review
from .forms import ProductForm, ReviewForm
from django.core.paginator import Paginator
from django.http import HttpResponseForbidden

def product_list(request):
    products = Product.objects.all()
    products = Product.objects.select_related("category", "seller").all()
    categories = Category.objects.all()
    
    q = (request.GET.get("q") or "").strip()
    if q:
        products = products.filter(title__icontains=q)

    category_id = (request.GET.get("category") or "").strip()
    if category_id.isdigit():
        products = products.filter(category_id=int(category_id))

    paginator = Paginator(products, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'products/product_list.html', {
        'page_obj': page_obj,
        "categories": categories,
        "q": q,
        "selected_category": category_id,
     })

def add_product(request):
         form = ProductForm(request.POST, request.FILES)
         if form.is_valid():
             product = form.save(commit=False)
             product.seller = request.user
             product.save()
             return redirect('product_list')

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
            return redirect('product_list')
    else:
        form = ProductForm(instance=product)
    
    return render(request, 'products/edit_product.html', {'form': form, 'product': product})

@login_required
def delete_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    
    if product.seller != request.user:
        return HttpResponseForbidden("You are not allowed")
    
    if request.method == 'POST':
        product.delete()
        return redirect('my_products')
    
    return render(request, 'products/delete_product.html', {'product': product})