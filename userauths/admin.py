from django.contrib import admin
from .models import User, Profile, ContactUs

# Register your models here.
class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'bio']

class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'full_name', 'image', 'phone']

class ContactUsAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'email', 'subject']

admin.site.register(User, UserAdmin)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(ContactUs, ContactUsAdmin)