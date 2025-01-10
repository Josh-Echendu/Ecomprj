from django.shortcuts import redirect
from django.contrib import messages

# Create a function in which only an admin can access
def admin_required(view_func):
    def wrapper(request, *args, **kwargs):

        # Check if user is not an admin
        if request.user.is_superuser != True:
            messages.warning(request, 'You are not authorized to access this page.')
            return redirect('/user/sign-in')
        return view_func(request, *args, **kwargs)
    
    return wrapper