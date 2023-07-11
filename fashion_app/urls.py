"""
URL configuration for man_fashion project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path
from . import views

urlpatterns = [
   path('', views.home, name='home'),
   path('register/',views.register,name='register'),
   path('login/',views.login,name='login'),
   path('otp/',views.otp,name="otp"),
   path('resend-email/<str:em>', views.resend_email, name='resend_email'),
   path('logout/', views.logout, name='logout'),
   path('profile/', views.profile, name='profile'),
   path('shop/', views.shop, name='shop'),
   path('shop_details/<int:pk>', views.shop_details, name='shop_details'),
   path('shopping_cart/<int:pk>', views.shopping_cart, name='shopping_cart'),
   path('cart/', views.cart, name='cart'),
   path('delete_cart/<int:pk>', views.delete_cart, name='delete_cart'),
   path('update_cart/', views.update_cart, name='update_cart'),
   path('search/', views.search, name='search'),
   path('checkout/', views.checkout, name='checkout'),
   path('paymenthandler/', views.paymenthandler, name='paymenthandler'),
   path('checkout_details/', views.checkout_details, name='checkout_details'),
    path('payment-response/', views.payment_response, name='payment_response'),

]
