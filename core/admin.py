from django.contrib import admin
from .models import Category, Tags, Vendor, Product
from .views import index
from django.urls import path
from .models import ProductImages, Cartorder, Cart, Coupon
from .models import CartOrderItems, ProductReview, Wishlist, Address 

# for eacg product we want to have multiple images
class ProductImagesAdmin(admin.TabularInline):
    model = ProductImages

class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImagesAdmin]
    list_display = ['user', 'title', 'product_image', 'price', 'category', 'vendor', 'featured', 'product_status']

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'category_image']

class VendorAdmin(admin.ModelAdmin):
    list_display = ['title', 'vendor_image']

class CartOrderAdmin(admin.ModelAdmin):
    list_editable = ['paid_status', 'Product_status'] # to edit a column
    list_display = ['user', 'price', 'paid_status', 'order_date', 'Product_status']

class CartOrderItemsAdmin(admin.ModelAdmin):
    list_display = ['order', 'invoice_no', 'item', 'image', 'price', 'total']

class ProductReviewAdmin(admin.ModelAdmin):
    list_display = ['user', 'product', 'review', 'rating']

class wishListAdmin(admin.ModelAdmin):
    list_display = ['user', 'product', 'date']

class AddressAdmin(admin.ModelAdmin):
    list_editable = ['address', 'status']
    list_display = ['user', 'address', 'status']

class CartAdmin(admin.ModelAdmin):
    list_display = ['product', 'quantity', 'price']



admin.site.register(Cartorder, CartOrderAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Vendor, VendorAdmin)
admin.site.register(CartOrderItems, CartOrderItemsAdmin)
admin.site.register(ProductReview, ProductReviewAdmin)
admin.site.register(Wishlist, wishListAdmin)
admin.site.register(Address, AddressAdmin)
admin.site.register(Cart)
admin.site.register(Coupon)

