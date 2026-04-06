from django.urls import path
from .views import product_list, product_detail, add_product

urlpatterns = [
    path('', product_list, name='product_list'),
    path('<int:pk>/', product_detail, name='product_detail'),
    path('add/', add_product, name='add_product'),
]

from .views import product_list, product_detail, add_product, my_products

urlpatterns = [
    path('', product_list, name='product_list'),
    path('add/', add_product, name='add_product'),
    path('my-products/', my_products, name='my_products'),
    path('<int:pk>/', product_detail, name='product_detail'),
]