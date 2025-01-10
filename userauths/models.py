from django.utils.html import mark_safe
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save

# we want to change django login admin field from 'username' to 'email', we want to keep loggin in with email &password
class User(AbstractUser):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=100)
    bio = models.CharField(max_length=100)
    
    #we change the login field from 'username' to 'email'
    USERNAME_FIELD = 'email'

    # we added the REQUIRED_FIELDS bcos to avoid an error, so that when we use the 'createsuperuser' functionality we would have 4 fields such as 'username', 'email', 'password1', 'password2'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return f'{self.username}'

class ContactUs(models.Model):
    full_name = models.CharField(max_length=200)
    email = models.CharField(max_length=200)
    phone = models.CharField(max_length=200)
    subject = models.CharField(max_length=200)
    message = models.TextField()

    
    class Meta:
        verbose_name_plural = 'Contact Us'


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='image')
    full_name = models.CharField(max_length=200, null=True, blank=True)
    bio = models.CharField(max_length=200, null=True, blank=True)
    phone = models.CharField(max_length=200)
    address = models.CharField(max_length=200, null=True, blank=True)
    country = models.CharField(max_length=200, null=True, blank=True)
    verifield = models.BooleanField(default=False)

    def Profile_image(self):
        # (self.image.url) is gonna replace '%s'
        return mark_safe('<img src="%s" width="50" height="50" />' % (self.image.url))

    def __str__(self):
        return self.full_name or self.user.username or "Profile"

# Purpose: This function ensures that whenever a new User object is created, a corresponding Profile object is also created automatically.  
def create_user_profile(sender, instance, created, **kwargs):
    if created:  # Check if this is a new user being created
        Profile.objects.create(user=instance)  # Create a Profile instance linked to this User

# Purpose: This function ensures that whenever a User object is updated, its associated Profile object is also saved.
#  This is helpful if you ever make changes to the User object that might indirectly affect the Profile and need to save it.
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

# instance.profile: This accesses the Profile associated with the User instance.
# .save(): This saves any changes made to the Profile.

# What This Does: These lines "connect" the signal functions (create_user_profile and save_user_profile)
#  to the post_save signal of the User model.
post_save.connect(create_user_profile, sender=User)
post_save.connect(save_user_profile, sender=User)