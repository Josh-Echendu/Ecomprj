from django.urls import path
from .views import profile_edit_view, register_view, login_view, logout_view


app_name = 'userauths'

urlpatterns = [
    path('sign_up/', register_view, name='sign-up'),
    path('sign_in/', login_view, name='sign-in'),
    path('sign_out/', logout_view, name='sign-out'),
    path('profile-edit/', profile_edit_view, name='profile-edit'),

]