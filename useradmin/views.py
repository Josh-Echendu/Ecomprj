from core.models import ProductReview
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from core.models import Cartorder, Product, Category, CartOrderItems
from django.db.models import Sum
from userauths.models import User
from django.contrib.auth.decorators import login_required
from useradmin.forms import ProductForm
from django.views.decorators.csrf import csrf_exempt
from userauths.models import Profile
from django.contrib.auth.hashers import check_password
from .decorators import admin_required

import datetime

@admin_required
def dashboard(request):
    
    # Get the total price of the cartorder that a store owner has
    revenue = Cartorder.objects.aggregate(price=Sum('price'))

    # Total order a store has
    total_order_count = Cartorder.objects.all().count()

    all_product = Product.objects.all().count()
    all_categories = Category.objects.all().count()
    new_customers = User.objects.all().order_by('-id')
    latest_orders = Cartorder.objects.all().order_by('-id')

    # Get monthly revenue
    this_month = datetime.datetime.now().month

    monthly_revenue = Cartorder.objects.filter(order_date__month=this_month).aggregate(price=Sum('price'))

    context = {
        'revenue':revenue,
        'total_order_count': total_order_count,
        'all_product': all_product,
        'all_categories': all_categories,
        'new_customers': new_customers,
        'latest_orders': latest_orders,
        'monthly_revenue': monthly_revenue,
    }

    return render(request, 'useradmin/dashboard.html', context)

@admin_required
def product(request):
    all_product = Product.objects.all().order_by('-id')
    all_categories = Category.objects.all()

    context = {
        'all_products': all_product,
        'all_categories': all_categories
    }
    return render(request, 'useradmin/products.html', context) 

@admin_required
def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            new_form = form.save(commit=False)
            new_form.user = request.user
            new_form.save()

            # To save the many to many fields known as tags
            form.save_m2m()
            messages.success(request, 'Product added successfully')
            return redirect('useradmin:dashboard')
    else:
        form = ProductForm()

    context = {
        'form': form,
        'product': product
    }

    return render(request, 'useradmin/add-product.html', context)

@admin_required
def update_product(request, pid):
    product = get_object_or_404(Product, pid=pid)
    print(product.tags.all())
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            new_form = form.save(commit=False)
            new_form.user = request.user
            new_form.save()
            form.save_m2m()  # Ensure many-to-many fields (tags) are saved
            messages.success(request, 'Product updated successfully')
            return redirect('useradmin:update-product', pid=product.pid)
        else:
            print(form.errors)  # Debugging invalid form submissions
    else:
        form = ProductForm(instance=product)

    context = {
        'form': form,
        'product': product
    }
    return render(request, 'useradmin/update-product.html', context)

@admin_required
def delete_product(request, pid):
    product = Product.objects.get(pid=pid)

    if product:
        product.delete()
        messages.success(request, 'Product deleted successfully')
        return redirect('useradmin:products')
    else:
        messages.error(request, 'Product doesn"t exist')
        return redirect('useradmin:products')

@admin_required
def orders_view(request):
    orders = Cartorder.objects.all().order_by('-id')

    context = {
        'orders': orders
    }

    return render(request, 'useradmin/orders.html', context)

@admin_required
def order_detail_view(request, oid):

    order = get_object_or_404(Cartorder, oid=oid)

    order_items = CartOrderItems.objects.filter(order=order)

    # if request.method == 'POST':
    #     status = request.POST.get('status')
    #     order.Product_status = status
    #     order.save()
    #     messages.success(request, f'product has being {order.Product_status}')

    context ={
        'order': order,
        'order_items': order_items,
    }

    return render(request, 'useradmin/order_detail.html', context)

@csrf_exempt
def change_order_status(request, oid):
    order = Cartorder.objects.get(oid=oid)
    print(order.Product_status)
    if request.method == 'POST':
        status = request.POST.get('status')
        order.Product_status = status
        order.save()
        messages.success(request, f'product has being {order.Product_status}')
    
    return redirect('useradmin:order-detail', order.oid)

@admin_required
def shop_page_view(request):
    products = Product.objects.all()
    revenue = Cartorder.objects.aggregate(price=Sum('price'))
    total_qty = CartOrderItems.objects.filter(order__paid_status = True).aggregate(qty=Sum('qty'))

    context ={
        'products': products,
        'revenue': revenue,
        'total_qty': total_qty
    }

    return render(request, 'useradmin/shop_page.html', context)

@admin_required
def reviews_view(request):
    reviews = ProductReview.objects.all()
    
    context ={
        'reviews': reviews,
    }

    return render(request, 'useradmin/reviews.html', context)

@admin_required
def profile_settings_view(request):
    profile = Profile.objects.get(user=request.user)
    
    if request.method == 'POST':
        image = request.FILES.get('image')
        full_name = request.POST.get('full_name')
        bio = request.POST.get('bio')
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        country = request.POST.get('country')

        if image is not None:
            profile.image = image

        profile.user = request.user
        profile.full_name = full_name
        profile.bio = bio
        profile.phone = phone
        profile.address = address
        profile.country = country
        profile.save()
        messages.success(request, 'Profile updated sucessfully!!!')
        return redirect('useradmin:profile-settings')
    
    context = {
        'profile': profile
    }
    return render(request, 'useradmin/profile-settings.html', context)


@admin_required
def change_password_view(request):
    user = request.user
    print(user)

    if request.method == 'POST':
        old_password = request.POST.get('old_password')
        new_password = request.POST.get('new_password')
        confirm_new_password = request.POST.get('confirm_new_password')

        if confirm_new_password != new_password:
            messages.warning(request, 'Password does not match')
            return redirect('useradmin:change-password')
        
        
        # Compare if old_password is the same as the password in the database
        if check_password(old_password, user.password):

            # Set new password
            user.set_password(new_password)
            user.save()
            messages.success(request, 'password changed succesfully')
            return redirect('useradmin:change-password')
        
        # elif old_password == new_password:
        #     messages.warning(request, 'old and new password are the same, please change it')
        #     return redirect('useradmin:change-password')

        else:
            messages.warning(request, 'Old password is incorrect')
            return redirect('useradmin:change-password')
    
    return render(request, 'useradmin/change-password.html')
