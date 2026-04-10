from django.urls import path
from .views import order_history, stripe_checkout, payment_success, order_detail

urlpatterns = [
    path('checkout/', stripe_checkout, name='stripe_checkout'),
    path('success/', payment_success, name='payment_success'),
    path('history/', order_history, name='order_history'),
    path('<int:pk>/', order_detail, name='order_detail'),
]