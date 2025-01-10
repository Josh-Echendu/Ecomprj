from django.urls import path
from .views import dashboard, change_password_view, profile_settings_view, product, add_product, update_product, change_order_status, delete_product, order_detail_view, orders_view, shop_page_view, reviews_view

app_name= 'useradmin'

urlpatterns = [
    path('dashboard/', dashboard, name='dashboard'),
    path('dashboard/products', product, name='products'),
    path('dashboard/add-products', add_product, name='add-products'),
    path('update_product/<pid>', update_product, name='update-product'),
    path('delete_product/<pid>', delete_product, name='delete-product'),
    path('orders/', orders_view, name='order'),
    path('order-detail/<oid>/', order_detail_view, name='order-detail'),
    path('change_order_status/<oid>', change_order_status, name='change_order_status'),
    path('shop_page/', shop_page_view, name='shop-page'),
    path('reviews/', reviews_view, name='reviews'),
    path('profile_settings/', profile_settings_view, name='profile-settings'),
    path('change_password/', change_password_view, name='change-password'),


]