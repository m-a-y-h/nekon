from django.db import ( models, )
from django.contrib.auth.models import ( AbstractBaseUser, PermissionsMixin, )
from django.utils.translation import ( gettext_lazy as _, )
from .managers import ( UserManager, )
from rest_framework_simplejwt.tokens import ( RefreshToken, )

AUTH_PROVIDERS = {'email':'email', 'google':'google', 'github':'github', 'facebook':'facebook', 'discord':'discord'}

# Custom user model inheriting from Django's AbstractBaseUser and PermissionsMixin
class User(AbstractBaseUser, PermissionsMixin):
    # Email field, used as the unique identifier for authentication
    email = models.EmailField(max_length=255, unique=True, verbose_name=_("Email Address"))
    
    # User's first name and last name fields
    first_name = models.CharField(max_length=100, verbose_name=_("First Name"))
    last_name = models.CharField(max_length=100, verbose_name=_("Last Name"))
    
    # Boolean flags indicating user status
    is_active = models.BooleanField(default=True)  # Whether the user is active or not
    is_staff = models.BooleanField(default=False)  # Whether the user is part of the staff
    is_superuser = models.BooleanField(default=False)  # If the user has all admin privileges
    is_verified = models.BooleanField(default=False)  # If the user's email is verified
    
    # Timestamps for when the user joined and last logged in
    date_joined = models.DateTimeField(auto_now_add=True)  # Automatically set at user creation
    last_login = models.DateTimeField(auto_now=True)  # Updated every time the user logs in

    auth_provider = models.CharField(max_length=50, default=AUTH_PROVIDERS.get("email"))

    # Setting the field used for authentication (email instead of username)
    USERNAME_FIELD = 'email'
    
    # Fields required when creating a superuser
    REQUIRED_FIELDS = ['first_name', 'last_name']

    # Custom manager for the User model
    objects = UserManager()

    # String representation of the user, returns the user's email
    def __str__(self):
        return self.email

    # Property to get the user's full name
    @property
    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

    # Method to generate JWT tokens (both access and refresh) for the user
    def tokens(self):
        refresh = RefreshToken.for_user(self)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        }

# Model for storing one-time password (OTP) associated with a user
class OneTimePassword(models.Model):
    # OTP is linked to a single user
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    
    # OTP code, stored as a unique 6-character string
    code = models.CharField(max_length=6, unique=True)

    # String representation of the OTP model, showing the user's first name and passcode
    def __str__(self):
        return f"{self.user.first_name} - passcode"