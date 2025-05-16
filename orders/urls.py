from django.urls import path
from .views import AddToCartView, CartView, CheckoutView, OrderHistoryView, AdminDashboardView

app_name = 'orders'

urlpatterns = [
    path('add/<int:pk>/', AddToCartView.as_view(), name='add_to_cart'),
    path('cart/', CartView.as_view(), name='cart'),
    path('checkout/', CheckoutView.as_view(), name='checkout'),
    path('history/', OrderHistoryView.as_view(), name='history'),
    path('dashboard/', AdminDashboardView.as_view(), name='dashboard'),
]
