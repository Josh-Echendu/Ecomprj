from django.urls import path, include
from .views import search_view, filter_product, index, category_listView, tag_list, vendor_detail_view, product_listView, product_detail_view, category_product_list_view, vendor_list_view, ajax_add_review
from .views import add_to_cart, delete_wishlist, cart_view, wish_list_view, add_wishlist_view, delete_cart_view, update_cart_view, checkout_view
from .views import payment_completed_view, payment_failed_view, customer_dashboard_view, order_detail_view, make_default_address
from .views import ajax_contact, save_check_out, create_ckeckout_session, Contact_Us_view, create_address

app_name = 'core'

urlpatterns = [

    # Home page
    path('', index, name='home'),
    path('products/', product_listView, name='product-list'),
    path('products/<pid>', product_detail_view, name='product-detail'),

    # category
    path('category/', category_listView, name='category-list'),
    path('category/<cid>/', category_product_list_view, name='category-product-list'),

    # vendor
    path('vendors/', vendor_list_view, name='vendor-list'),
    path('vendors/<vid>', vendor_detail_view, name='vendor-detail'),

    # Tags
    path('products/tag/<slug:tag_slug>/', tag_list, name='tag-list'),

    # Add Reviews
    path('ajax_add_review/<pid>', ajax_add_review, name='ajax-add-review'),
    path('search/', search_view, name='search'),

    # filter products
    path('filter-products/', filter_product, name='filter'),

    # Add to cart
    path('add-to-cart/<int:product_id>/', add_to_cart, name='add_to_cart'),

    # Cart view
    path('cart/', cart_view, name='cart'),

    # Delete Cart
    path('delete_cart_item/<int:cart_item_id>/', delete_cart_view, name='delete_cart_item'),

    # update Cart
    path('update-cart_item/', update_cart_view, name='update_cart_item'),

    # Checkout Page
    path('checkout/<oid>', checkout_view, name='check_out'),
    
    # Paypal URL
    path('paypal/', include('paypal.standard.ipn.urls')),

    # Payment successfull
    path('payment-completed/<oid>/', payment_completed_view, name='payment-completed'),
    # path('payment-completed/<oid>/', payment_completed_view, name='payment-completed'),

    # Payment failed
    path('payment-failed/', payment_failed_view, name='payment-failed'),

    # User Dashboard
    path('dashboard/', customer_dashboard_view, name='dashboard'),

    # Dashboard Detail
    path('dashboard/order/<int:pk>', order_detail_view, name='order_detail'),

    # Default Address
    path('make-default-address/', make_default_address, name='default-address'),
    path('create-address/', create_address, name='create-address'),


    # Wishlist view
    path('wishlist/', wish_list_view, name='wishlist'),

    # Add to Wishlist 
    path('add-to-wishlist/', add_wishlist_view, name='add-to-wishlist'),

    # Delete Wishlist
    path('wishlist_delete/', delete_wishlist, name='delete-wishlist'),

    # Contact View
    path('contact/', Contact_Us_view, name='contact'),

    # Ajax contact view     
    path('ajax-contact-form/', ajax_contact, name='ajax-contact'),

    # order and order_item checkout
    path('save_check_out_info/', save_check_out, name='save_check_out'),

    # Stripe url
    path('api/create_checkout_session/<oid>/', create_ckeckout_session, name='create_ckeckout_session'),
]
