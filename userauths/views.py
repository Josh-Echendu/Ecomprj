from django.http import HttpResponseRedirect
from .forms import ProfileForm
from django.http import JsonResponse
from django.shortcuts import render, redirect
from userauths.forms import UserRegistrationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.conf import settings
from .models import User, Profile

# Create your views here.
def register_view(request):
    
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST or None)
        if form.is_valid():
            new_user = form.save()

            # Extract the username
            username = form.cleaned_data.get('username')

            # success message
            messages.success(request, f"Hey {username}, Your account was created succesfully")

            # To login automatically without directing you to the login page 
            new_user = authenticate(username=form.cleaned_data['email'],
            password=form.cleaned_data['password1']
            )
            login(request, new_user)
            return redirect('core:home')

    else:
        form = UserRegistrationForm()

    context = {
        'form': form
    }
    return render(request, 'userauth/sign-up.html', context)

def login_view(request):

    # To check if user is logged in, cos we dont want them to access the login pages again after logging in 
    if request.user.is_authenticated:
        messages.warning(request, f'Hey you are already logged in')
        return redirect('core:home')
    
    if request.method == 'POST':

        # Extract the users data from the form 
        email = request.POST.get('email')
        password = request.POST.get('password')

        # To check if the form data matches with the data in the database
        try:
            user = User.objects.get(email=email)

            # To log the user in if there is actually a user with such email and password 
            user = authenticate(request, email=email, password=password) #The authenticate method has a field called email and password

            if user is not None: # if there is actually a user
                login(request, user)
                messages.success(request, 'you are logged in.')

                #extracts the value of next from the query string (/wishlist/ in this case).
                # If the next parameter is not present in the URL, it defaults to '/' (the homepage or any other default value you specify).
                next_url = request.GET.get('next', '/')

                return HttpResponseRedirect(next_url)
                # return redirect('core:home')
            else: # if user does not exist
                messages.warning(request, 'User Does not exist, create an account.')

        except:
            messages.warning(request, f'User with {email} does not exist')

    return render(request, 'userauth/sign-in.html')

def logout_view(request):
    logout(request)
    messages.success(request, "you've  being logged out")
    return redirect('userauths:sign-in')

def profile_edit_view(request):
    profile = Profile.objects.get(user=request.user)
    
    if request.method == 'POST':

        # we using request.Files bcos we are collecting an image file 
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            new_form = form.save(commit=False) # not commiting to the database yet
            new_form.user=request.user
            new_form.save()
            messages.success(request, 'Profile Updated successfully.')
            return redirect('core:dashboard')
    
    else:
        form = ProfileForm(instance=profile) 

    context ={
        'form': form,
        'profile': profile
    }
    return render(request, 'userauth/profile-edit.html', context)
