from django.urls import path
from . import views

urlpatterns = [
   path('index/', views.seller_index, name='seller_index'),
   path('seller_register/',views.seller_register,name='seller_register'),
   path('seller_login/',views.seller_login,name='seller_login'),
   path('seller_otp/',views.seller_otp,name="seller_otp"),
   path('resend-seller_resend_email/<str:em>', views.seller_resend_email, name='seller_resend_email'),
   path('seller_logout/', views.seller_logout, name='seller_logout'),
   path('seller_profile/', views.seller_profile, name='seller_profile'),
   path('seller_listing/', views.seller_listing, name='seller_listing'),
   path('all_listing/', views.all_listing, name='all_listing'),
   path('seller_listing_update/<int:pk>', views.seller_listing_update, name='seller_listing_update'),
   path('delete/<int:pk>', views.delete, name='delete'),
]