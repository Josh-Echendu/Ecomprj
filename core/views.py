from taggit.models import Tag
from django.shortcuts import get_object_or_404
from django.shortcuts import render, HttpResponse, redirect
from django.http import JsonResponse
from django.template.loader import render_to_string
from .models import ProductImages, Cartorder
from .models import CartOrderItems, Coupon, ProductReview, Wishlist, Address 
from .models import Category, Tags, Vendor, Product, Cart
from django.db.models import Count, Avg, Q, Sum
from .forms import ProductReviewForm
from django.urls import reverse_lazy
from django.views.generic import DeleteView
from django.contrib import messages
from userauths.models import Profile, ContactUs
from django.db import transaction


from django.urls import reverse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from paypal.standard.forms import PayPalPaymentsForm

import stripe
import calendar
from django.db.models.functions import ExtractMonth

# Create your views here.
def index(request):
    products = Product.objects.filter(product_status='pubished', featured=True).order_by('-id')

    context = {
        'products': products
    }

    return render(request, 'core/index.html', context)


def product_listView(request):
    
    products = Product.objects.filter(product_status='pubished').order_by('-id')

    context = {
        'products': products
    }

    return render(request, 'core/product-list.html', context)


def category_listView(request):

    categories = Category.objects.all()

    context = {
        'categories':categories,
    }
    return render(request, 'core/category-list.html', context)


def category_product_list_view(request, cid):


    # either cosmetics or food
    category = Category.objects.get(cid=cid)

    # Extract all products for each category
    products = Product.objects.filter(product_status='pubished', category=category)

    context = {
        'category':category,
        'products':products,
    }

    return render(request, 'core/category-product-list.html', context)

def vendor_list_view(request):

    vendors = Vendor.objects.all()

    context = {
        'vendors': vendors
    }
    return render(request, 'core/vendor-list.html', context)

def vendor_detail_view(request, vid):
    
    vendor = Vendor.objects.get(vid=vid)

    # Extract all the products of a particular vendor that is published
    products = Product.objects.filter(product_status='pubished', vendor=vendor)

    context = {
        'vendor':vendor,
        'products': products
    }
    return render(request, 'core/vendor-detail.html', context)

def product_detail_view(request, pid):
    
    # Extract the single record with the pid
    product = Product.objects.get(pid=pid)
    
    # Extract all the products whose category is equal to the 
    products = Product.objects.filter(category=product.category).exclude(pid=pid)

    # product review form
    review_form = ProductReviewForm()

    # if a user has created a comment for a particular product we dont want them to ever comment on that product 
    make_review = True

    if request.user.is_authenticated:

        # Count the amount of reviews
        user_review_count = ProductReview.objects.filter(user=request.user, product=product).count()

        if user_review_count > 0:
            make_review = False

    # Reviews for each product
    reviews = ProductReview.objects.filter(product=product).order_by('-id')

    # Getting average review calculation
    average_rating = ProductReview.objects.filter(product=product).aggregate(rating=Avg('rating'))

    # Extract all the product image of a particular products 
    product_images = product.p_images.all()

    
    context = {
        'product':product,
        'p_images': product_images,
        'make_review': make_review,
        'review_form': review_form,
        'average_rating': average_rating,
        'reviews': reviews,
        'products': products
    }
    return render(request, 'core/product-detail.html', context)

def tag_list(request, tag_slug=None):
    products = Product.objects.filter(product_status='pubished').order_by('-id')

    tag = None
    if tag_slug:
        # Note: the Tag model has a field called slug
        tag = get_object_or_404(Tag, slug=tag_slug)

        # Get all the product related to the slug
        # Filter out all the products related to a particular tag 
        products = products.filter(tags__in=[tag])

    context = {
        'products':products,
        'tag': tag
    }
    return render(request, 'core/tag_list.html', context)

def ajax_add_review(request, pid):

    # Get the product
    product = Product.objects.get(pid=pid)
    
    # Get the logged in user
    user = request.user

    review = ProductReview.objects.create(
        user=user,
        product=product,
        review = request.POST['review'],
        rating = request.POST['rating'],
    )

    context = {
        'user': user.username,
        'review': request.POST['review'],
        'rating': request.POST['rating'],

    }

    average_reviews = ProductReview.objects.filter(product=product).aggregate(rating=Avg('rating'))

    return JsonResponse(
        {        
            'bool': True,
            'context': context,
            'average_reviews': average_reviews
        }
    )



def search_view(request):
    query = request.GET.get('q')

    # Fiter by title and description | icontains is a builtin django function which is used to get related things to what you searching or we can use 'title__startswith' to search for the starting of any word 
    products = Product.objects.filter(title__icontains=query).order_by('-date')

    context = {
        'products': products,
        'query': query,
    }

    return render(request, 'core/search.html', context)

def filter_product(request):

    # Extract the list or array of clicked checkbox for categories
    categories = request.GET.getlist('category[]') #'.getlist' is used for extracting the clicked checkbox/data from a list or array

    # # Extract the list or array of clicked checkbox for vendors 
    vendors = request.GET.getlist('vendor[]')

    min_price = request.GET['min_price']
    max_price = request.GET['max_price']

    products = Product.objects.filter(product_status='pubished').order_by('-id').distinct()

    products = products.filter(price__gte=min_price)
    products = products.filter(price__lte=max_price)
    
    # Filter out the product based on the category clicked on
    if len(categories) > 0:

        # category_id_in: this means check if the products category_id is in categories list
        products = products.filter(category__id__in=categories).distinct()

    # Filter out the product based on the vendor clicked on
    if len(vendors) > 0:

        # vendor_id_in: this means check if the product vendor_id is in vendors 
        products = products.filter(vendor__id__in=vendors).distinct()

    context = {
        'products': products
    }

    data = render_to_string('core/async/product-list.html', context)

    return JsonResponse({'data': data})



from django.http import JsonResponse
from django.db.models import Sum, F
from .models import Product, Cart

def add_to_cart(request, product_id):
    if request.user.is_authenticated:
        user = request.user

        # Retrieve quantity and price from request
        try:
            quantity = int(request.GET.get('qty', 1))  # Default quantity to 1
            price = float(request.GET.get('price'))
        except (ValueError, TypeError):
            return JsonResponse({'error': 'Invalid quantity or price'}, status=400)

        # Retrieve product information
        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return JsonResponse({'error': 'Product not found'}, status=404)

        # Check if item already exists in the cart
        existing_cart_item = Cart.objects.filter(user=user, product=product).first()

        if existing_cart_item:
            existing_cart_item.quantity += quantity  # Increment quantity
            existing_cart_item.price = price
            existing_cart_item.save()
            messages.warning(request, 'Cart updated')
        else:
            Cart.objects.create(user=user, product=product, quantity=quantity, price=price)
            messages.success(request, 'Item added to cart')

        # Calculate total items and subtotal
        cart_items = Cart.objects.filter(user=user)
        total_item = cart_items.count()

        return JsonResponse({
            'status': 'success',
            'total_item': total_item,
            'id': product_id,
            # 'cart_subtotal': round(cart_subtotal, 2)
        })
    else:
        return JsonResponse({'error': 'User not authenticated'}, status=401)

@login_required
def cart_view(request):
    cart_items = Cart.objects.filter(user=request.user)
    count = cart_items.count()

    total_subtotal = sum(item.multiply_price() for item in cart_items)
    context = {
        'cart_items': cart_items,
        'total_subtotal': total_subtotal,
        'count': count,
    }

    return render(request, 'core/cart.html', context)


def delete_cart_view(request, cart_item_id):

    # Get the cart item by ID or return a 404 if not found
    cart_item = get_object_or_404(Cart, id=cart_item_id, user=request.user)
    
    # Delete the cart item
    cart_item.delete()

    # Calculate the updated totals
    cart_items = Cart.objects.filter(user=request.user)
    total_subtotal = sum(item.price * item.quantity for item in cart_items)
    total_items = cart_items.count()

    # Return the updated totals as JSON
    return JsonResponse({
        'status': 'success',
        'total_subtotal': total_subtotal,
        'total_items': total_items
    })

def update_cart_view(request):

    id = str(request.GET.get('id'))
    qty = request.GET.get('qty')
    print(qty)

    cart_item = get_object_or_404(Cart, pk=id)

    cart_item.quantity = qty

    cart_item.save()

    # cart_items = Cart.objects.filter(user=request.user)
    quantity = cart_item.quantity
    cart_items = Cart.objects.filter(user=request.user)
    sub_total = sum(item.price * item.quantity for item in cart_items)
    total_price = cart_item.multiply_price()
    print(total_price)

    return JsonResponse(
        {
            'status': 'success',
            'new_quantity': quantity,
            'price': f"$ {total_price}",
            'subtotal': f"$ {sub_total}"
        }
)


# We want it that when we create an order item it redirects us to the checkout page 

def save_check_out(request):
    if request.method == 'POST':

        # Extract all the carts for a particular user
        cart_items = Cart.objects.filter(user=request.user)
        
        # Handle case where cart is empty
        if not cart_items.exists():
            return redirect('core:cart')  # Redirect to the cart view or an error page

        # Calculate total amount from cart items
        total_amount = sum(item.multiply_price() for item in cart_items)

        # Retrieve form data
        full_name = request.POST.get('full_name')
        email = request.POST.get('email')
        mobile = request.POST.get('mobile')
        address = request.POST.get('address')
        city = request.POST.get('city')
        state = request.POST.get('state')
        country = request.POST.get('country')

        # Save order data in an atomic transaction
        with transaction.atomic():
            
            # Create order
            order = Cartorder.objects.create(
                user=request.user,
                price=total_amount,
                full_name=full_name,
                email=email,
                mobile=mobile,
                address=address,
                city=city,
                state=state,
                country=country,
            )

            # Save cart items as order items (cart remains untouched)
            for item in cart_items:
                CartOrderItems.objects.create(
                    order=order,
                    invoice_no=f"INVOICE_NO-{order.id}",
                    item=item.product.title,
                    image=item.product.image,
                    qty=item.quantity,
                    price=item.price,
                    total=item.multiply_price(),
                )

            # # Optionally clear the cart after checkout
            # cart_items.delete()

        return redirect('core:check_out', oid=order.oid)

    # Handle non-POST requests or unexpected cases
    return redirect('core:cart')  # Redirect to cart or appropriate error page


def checkout_view(request, oid):
    order = Cartorder.objects.get(oid=oid)
    order_items = CartOrderItems.objects.filter(order=order)

    if request.method == 'POST':
        code = request.POST.get('code')
        print(code)
        coupon = Coupon.objects.filter(code=code, active=True).first()
        
        # if coupon Exists 
        if coupon: 
            # if coupon exist in the manyTomany field coupon
            if coupon in order.coupons.all():
                messages.warning(request, 'Coupon already activated')
                return redirect('core:check_out', order.oid)
            else:
                # Calculate the discount 
                discount = order.price * coupon.discount / 100
                
                # Add new coupon to avoid users activating a coupon more than ones
                order.coupons.add(coupon)

                # price - discount
                order.price -= discount

                # discount percentage price
                order.saved += discount
                order.save()

                messages.success(request, 'Coupon Activated')
                return redirect('core:check_out', oid=order.oid)
        else:
            messages.warning(request, 'Coupon Does Not Exist')
            return redirect('core:check_out', oid=order.oid)

    context = {
        'order': order,
        'order_items': order_items,
        'stripe_publishable_key': settings.STRIPE_PUBLIC_KEY
    }

    return render(request, 'core/checkout.html', context)

@csrf_exempt
def create_ckeckout_session(request, oid):
    print(oid)
    order = Cartorder.objects.get(oid=oid)
    stripe.api_key = settings.STRIPE_SECRET_KEY

    # Create new checkout session
    checkout_session = stripe.checkout.Session.create(
        customer_email = order.email,
        payment_method_types = ['card'],
        line_items = [
            {
                'price_data': {
                    'currency': 'USD',
                    'product_data': {
                        'name': order.full_name,
                    },
                    'unit_amount': int(order.price * 100)
                },
                'quantity': 1
            }
        ],
        mode =  'payment',

        success_url = request.build_absolute_uri(reverse('core:payment-completed', args=[str(order.oid)])) + '?session_id={CHECKOUT_SESSION_ID}',
        cancel_url = request.build_absolute_uri(reverse('core:payment-failed'))

    )
    order.paid_status = False
    order.stripe_payment = checkout_session['id']
    order.save()

    return JsonResponse({'sessionId': checkout_session.id})

@login_required
def payment_completed_view(request, oid):
    order = Cartorder.objects.get(oid=oid)
    if order.paid_status == False:
        order.paid_status = True
        order.save()
        Cart.objects.filter(user=request.user).delete()

    context = {
        'order':order,
    }
    return render(request, 'core/payment-completed.html', context)

@login_required
def payment_failed_view(request):
    return render(request, 'core/payment-failed.html')

@login_required
def customer_dashboard_view(request):

    # list of orders
    order_list = Cartorder.objects.filter(user=request.user).order_by('-id')

    # Addresses
    addresses = Address.objects.filter(user=request.user)

    # profile
    profile = Profile.objects.get(user=request.user)
    print(profile)

    # Extract the values of month and total number of cartorders in a list of dictionaries
    orders = Cartorder.objects.annotate(month=ExtractMonth('order_date')).values('month').annotate(count=Count('id')).values('month', 'count')

    month = []
    total_orders = []

    for o in orders:

        # tO APPEND THE NAME OF THE MONTH
        month.append(calendar.month_name[o['month']])

        # tO APPEND THE NUMBER OF ORDERS FOR A PARTICULAR MONTH
        total_orders.append(o['count'])

    else:
        print('Error: this is not a POST method')

    context = {
        'order_list': order_list,
        'address': addresses,
        'profile': profile,
        'orders': orders,
        'month_labels': month,
        'total_orders': total_orders,
    }
    return render(request, 'core/dashboard.html', context)

def create_address(request):
    if request.method == 'POST':
        address = request.POST.get('address')
        mobile = request.POST.get('mobile')

        Address.objects.create(
            user=request.user,
            address=address,
            mobile=mobile, 
        )
        messages.success(request, 'Address Added successfully.')
        return redirect('core:dashboard')

# def customer_dashboard_view(request):
#     if not request.user.is_authenticated:
#         return redirect('login')

#     # Orders
#     orders = Cartorder.objects.filter(user=request.user).order_by('-id')

#     # Addresses
#     addresses = Address.objects.filter(user=request.user)

#     # Get or create the Profile
#     profile, created = Profile.objects.get_or_create(user=request.user)

#     if request.method == 'POST':
#         address = request.POST.get('address')
#         mobile = request.POST.get('mobile')

#         Address.objects.create(
#             user=request.user,
#             address=address,
#             mobile=mobile, 
#         )
#         messages.success(request, 'Address added successfully.')
#         return redirect('core:dashboard')

#     context = {
#         'orders': orders,
#         'address': addresses,
#         'profile': profile
#     }
#     return render(request, 'core/dashboard.html', context)


def order_detail_view(request, pk):

    # Get the users order
    order = get_object_or_404(Cartorder, user=request.user, pk=pk)

    # Extract all the order items for a particular order
    order_items = CartOrderItems.objects.filter(order=order)

    context = {
        'order_items': order_items
    }
    return render(request, 'core/order-detail.html', context)


def make_default_address(request):
    id = request.GET.get('id')
    
    # Convert all address status to false for the current logged in user
    Address.objects.update(user=request.user, status=False)

    # update the status of a particular 
    Address.objects.filter(id=id).update(status=True)


    return JsonResponse(
        {
            'status': 'success'       
        }
    )

@login_required
def wish_list_view(request):

    try:
        wishlist = Wishlist.objects.filter(user=request.user)
    except:
        wishlist = None

    context = {
        'wishlist': wishlist
    }

    return render(request, 'core/wishlist.html', context)


@login_required
def add_wishlist_view(request):
    product_id = request.GET.get('id')  # Use .get to avoid KeyError
    
    if not product_id:
        return JsonResponse({'error': 'Product ID is required'}, status=400)
    
    try:
        product = Product.objects.get(id=product_id)
    except Product.DoesNotExist:
        return JsonResponse({'error': 'Product not found'}, status=404)
    
    # Check if the product is already in the wishlist to Avoid duplicate entries by checking existence
    wishlist_item, created = Wishlist.objects.get_or_create(user=request.user, product=product)
    
    if created: # created is a boolean either true or false
        messages.success(request, "Product added to wishlist.")
    else:
        messages.warning(request, "Product already in wishlist.")

    # Calculate the total number of items in the user's wishlist
    total_wishlist = Wishlist.objects.filter(user=request.user).count()

    return JsonResponse(
        {
            'status': 'success',
            'total_wishlist': total_wishlist,
        }
    )

def delete_wishlist(request):

    id = str(request.GET.get('id'))
    print(id)

    wishlist = get_object_or_404(Wishlist, pk=id, user=request.user)

    wishlist.delete()

    return JsonResponse({
        'status': 'success'
    })

def Contact_Us_view(request):
    return render(request, 'core/contact.html')

def ajax_contact(request):
    full_name = request.GET.get('full_name'),
    email = request.GET.get('email'),
    phone = request.GET.get('phone'),
    subject = request.GET.get('subject'),
    message = request.GET.get('message'),
    
    ContactUs.objects.create(full_name=full_name, email=email, phone=phone, subject=subject, message=message)

    return JsonResponse({
        'status': 'success',
        'message': 'Message sent successfully'
    })

