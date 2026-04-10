from django.urls import path
from . import views
from .views import add_review, delete_product, edit_product, product_list, product_detail, add_product

urlpatterns = [
    path('', views.product_list, name='product_list'),
    path('<int:pk>/', views.product_detail, name='product_detail'),
    path('<int:pk>/add-review/', views.add_review, name='add_review'),
]

from .views import product_list, product_detail, add_product, my_products

urlpatterns = [
    path('', product_list, name='product_list'),
    path('add/', add_product, name='add_product'),
    path('my-products/', my_products, name='my_products'),
    path('<int:pk>/', product_detail, name='product_detail'),
    path('<int:pk>/review/', add_review, name='add_review'),
    path('edit/<int:pk>/', edit_product, name='edit_product'),
    path('delete/<int:pk>/', delete_product, name='delete_product'),
]