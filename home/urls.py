from django.urls import path 
from . import views

urlpatterns = [
    path('', views.listHome.as_view(), name='home'),
    path('products/<int:cat_id>', views.show_product, name='products'),
    path('login/', views.loginUser.as_view(), name='login'),
    path('register/', views.register.as_view(), name='register'),
    path('logout/', views.logoutUser.as_view() ,name='logout'),
    path('detail/<int:pro_id>', views.show_product_detail, name='detail'),
    path('add_to_cart', views.updateItem, name='addcart'),
    path('cart/', views.cart, name='cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('process_order/', views.processOrder, name='process_order'),
    path('search/', views.seachProduct, name='search'),
    path('contact/', views.contact, name='contact'),

]