from unicodedata import name
from django.urls import path, include


from .views import  CheckoutView, ItemDetailView, ItemList, add_coupon,add_to_cart, OrderSummaryView, remove_from_cart,remove_single_item_from_cart
from django.shortcuts import render
app_name = "core"
urlpatterns = [
    path('',ItemList.as_view(),name='item-list'),
#    path('checkout/',lambda request: render(request,'checkout-page.html'),name='checkout'),
    path('product/add-to-cart/<slug>/', add_to_cart,name='add-to-cart'),
    path('product/remove-from-cart/<slug>/', remove_from_cart,name='remove-from-cart'),
    path('product/<slug>/', ItemDetailView.as_view(),name='item-detail'),
    path('order-summary/', OrderSummaryView.as_view(),name='order-summary'),
    path('remove-item-from-cart/<slug>/', remove_single_item_from_cart,
     name='remove-single-item-from-cart'),
    path('checkout/', CheckoutView.as_view(), name="checkout"),
    path('add-coupon/',add_coupon , name="add-coupon")

]
"""     path('payment/',CreatePayment.as_view(), name="payment"),
    path('payment-confirm/',PaymentConfirmation.as_view(), name="payment-confirmation"),
    path("payment-status/<int:pk>/",PaymentStatus.as_view(),name="payment-status"), """
