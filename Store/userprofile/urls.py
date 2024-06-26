from django.contrib.auth import views as auth_views
from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('myaccount/', views.myaccount, name="myaccount"),
    path('vendors/<int:pk>/', views.vendor_detail, name='vendor_detail'),
    path('login/', auth_views.LoginView.as_view(template_name='userprofile/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('my-shop/', views.my_shop, name='my_shop'),
    path('my-shop/add-product/', views.add_product, name='add_product'),
    path('my-shop/order-detail/<int:pk>/', views.my_shop_order_detail, name='my_shop_order_detail'),
    path('my-shop/edit-product/<int:pk>/', views.edit_product, name='edit_product'),
    path('my-shop/delete-product/<int:pk>/', views.delete_product, name='delete_product'),
]
