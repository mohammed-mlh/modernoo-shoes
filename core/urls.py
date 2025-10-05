from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('category/<int:category_id>/', views.category_page, name='category_detail'),
    path('cart/', views.cart_view, name='cart'),
    path('checkout/', views.checkout_view, name='checkout'),
    path('api/cart/add/', views.add_to_cart, name='add_to_cart'),
    path('api/cart/update/', views.update_cart_item, name='update_cart_item'),
    path('api/cart/remove/', views.remove_from_cart, name='remove_from_cart'),
    path('api/create-order/', views.create_order, name='create_order'),
    path('api/product-sizes/', views.get_product_sizes, name='get_product_sizes'),
]