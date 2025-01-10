from .models import Wishlist, Category, Vendor, Product, Cart, Address
from django.db.models import Min, Max
from django.contrib import messages
from django.shortcuts import redirect

def default(request):
    categories = Category.objects.all()
    vendors = Vendor.objects.all()
    min_max_price = Product.objects.aggregate(Min('price'), Max('price'))

    cart_items = None
    total_items = 0
    total_price = 0.0
    address = None
    wishlist = 0 # Set wishlist = 0 to ensure it always has a value, even for unauthenticated users.

    if request.user.is_authenticated:
        try:
            cart_items = Cart.objects.filter(user=request.user)
            total_items = cart_items.count()
            total_price = sum(item.price * item.quantity for item in cart_items)
        except Exception as e:
            print(f"Error fetching cart items: {e}")

        try:
            address = Address.objects.filter(user=request.user)
        except Address.DoesNotExist:
            address = None

        try:
            wishlist = Wishlist.objects.filter(user=request.user).count()
        except Wishlist.DoesNotExist:
            messages.warning(request, 'You need to log in to access wishlist')
            wishlist = 0 # Initialize wishlist with a default value
            return redirect('userauths: sign-in')


    return {
        'categories': categories,
        'vendors': vendors,
        'min_max_price': min_max_price,
        'cart_items_context': cart_items,
        'cart_total_items': total_items,
        'cart_total_price': total_price,
        'address': address,
        'wishlist': wishlist,
    }
