from django.urls import path
from .views import checkout, order_history

urlpatterns = [
    path('checkout/', checkout, name='checkout'),
    path('history/', order_history, name='order_history'),
]