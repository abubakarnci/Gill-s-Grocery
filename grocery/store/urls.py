from django.urls import path
from . import views

urlpatterns =[
    
    # leave as empty string from home page
    path('', views.store, name="store"),
    path('cart/', views.cart, name="cart"),
    path('checkout/', views.checkout, name="checkout"),
    ]