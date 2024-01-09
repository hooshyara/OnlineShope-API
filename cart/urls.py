from django.urls import path
from .views import CartView, CheckOut

app_name = 'cart'

urlpatterns = [
    path('cart/', CartView.as_view(), name='cart_detail'),
    path('<int:id>/cart/', CartView.as_view(), name='cart'),
    path('checkOut/', CheckOut.as_view(), name='CheckOut'),




] 