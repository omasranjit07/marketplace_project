from django.urls import path
from .views import product_list, product_detail, add_product, my_products, add_review, edit_product, delete_product

urlpatterns = [
    path('', product_list, name='product_list'),
    path('add/', add_product, name='add_product'),
    path('my-products/', my_products, name='my_products'),
    path('<int:pk>/', product_detail, name='product_detail'),
    path('<int:pk>/review/', add_review, name='add_review'),
    path('edit/<int:pk>/', edit_product, name='edit_product'),
    path('delete/<int:pk>/', delete_product, name='delete_product'),
]
