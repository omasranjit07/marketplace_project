from django.urls import path
from . import views
from .views import delete_product, edit_product, product_list, add_product

urlpatterns = [
    path('', views.product_list, name='product_list'),
    path('add/', views.add_product, name='add_product'),  # type: ignore[arg-type]
    path('my-products/', views.my_products, name='my_products'),
    path('edit/<int:pk>/', views.edit_product, name='edit_product'),
    path('delete/<int:pk>/', views.delete_product, name='delete_product'),
]